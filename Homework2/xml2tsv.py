import sys
from lxml import etree
# from helper import printf
import pandas as pd


def get_mtime(tree):
    '''
    Returns a dictionary: {k,v}
    k: Inode numbers
    v: Corresponding modification times
    '''
    l = tree.xpath('//INodeSection/inode/*[self::id or self::mtime]/text()')
    inodes,mtimes = l[::2],l[1::2]

    def timeformat(v):
        '''Return formatted time: month/day/year Hour:Minutes'''
        
        time = pd.to_datetime(v,unit='ms')
        mtime = time.strftime("%m/%d/%Y %H:%M")
        return mtime
    
    mtime_map = {k:timeformat(v) for k,v in zip(inodes,mtimes)}
    return mtime_map


def get_permissions(tree):
        '''Returns a dictionary: {k,v}
        k: Inode numbers
        v: Corresponding Permissions'''
        l = tree.xpath('//INodeSection/inode/*[self::id or self::permission or self::type]/text()')
        perm_map = {}
        num_map = {
                    '0':'---',
                    '2':'-w-',
                    '3':'-wx',
                    '4':'r--',
                    '5':'r-x',
                    '6':'rw-',
                    '7':'rwx' 
        }

        inode,ftype,perm = 0,1,2
        while(inode<len(l)):  

            s = ''
            if l[ftype] == "FILE": s+='-'
            else: s+='d' 
            n = l[perm].split(":")[2][1:]
            s+=''.join([num_map[user] for user in n])
            perm_map[l[inode]] = s
            inode+=3
            ftype+=3
            perm+=3
    
        return perm_map


def get_names(tree):
    '''This function returns root node and a dictionary: {k,v}
    k:Inode Number
    v:Corresponding name of the inode'''
    
    l = tree.xpath('//INodeSection/inode/*[self::id or self::name]/text()')
    root = tree.xpath('//INodeSection/inode[name[not(node())]]/id/text()')[0]
    l.remove(root)
    it = iter(l)
    name_map = dict(zip(it,it))
    name_map[root] = ''
    return root,name_map



def get_path(root,tree):
    '''Inputs: Root inode, tree
       Returns a dictionary: {k:v}
       k: inode number
       v: path to the key inode
    '''
    e = tree.xpath('//INodeDirectorySection/directory/*[self::parent or self::child]')
    dstruct = {} #Maintains child:parent pairs
    for i in e: 
        if i.tag == "parent": p = i.text 
        else: dstruct[i.text] = p #dstruct[child] = parent
    
    dstruct[root] = ''
    path_map = {root:''}
    for k in sorted(name_map)[1:]:   
        path_map[k] = path_map[dstruct[k]] + '/' + name_map[k]

    path_map[root] = '/'
    return path_map


def get_block_metadata(tree):
    '''This function returns two dictionaries:
    size_map: {k,v}, k = inode numbers, v=Corresponding file size
    block_map: {k,v}, k = inode numbers,v=Corresponding block count'''
    
    size_map = {}
    block_map = {}
    for ele in tree.xpath('//INodeSection/inode[blocks]/*[self::id or descendant::block]'):
        if ele.tag == "id": inode = ele.text
        if ele.tag == "blocks":
            size_map[inode],block_map[inode] = 0,0
            for block in ele.findall('block'):
                size_map[inode] += int(block.find('numBytes').text)
                block_map[inode] += 1
                
    return size_map,block_map


if __name__=="__main__":
    tree = etree.parse(sys.argv[1])
    
    #Getting modification times
    mtime_map = get_mtime(tree)
    
    #Getting permissions
    perm_map = get_permissions(tree)
    
    #Getting name
    root,name_map = get_names(tree)
    
    #Getting path
    path_map = get_path(root,tree)
    
    #Getting filesize and block count
    size_map,block_map = get_block_metadata(tree)
    
    #Getting everything together
    df = pd.DataFrame({"Path":path_map,"ModificationTime":mtime_map,"BlocksCount":block_map,"FileSize":size_map,"Permission":perm_map})
    df["BlocksCount"].fillna(value=0,inplace=True)
    df["FileSize"].fillna(value=0,inplace=True)
    df['BlocksCount'] = df['BlocksCount'].astype('int64')
    df['FileSize'] = df['FileSize'].astype('int64')
    
    print("Pandas DataFrame: \n\n")
    print(df.reset_index().drop('index',axis=1))
    
    #To tsv file
    df.to_csv(sys.argv[2],sep="\t",index=False)
    tsv = pd.read_csv(sys.argv[2],sep="\t")
    print("\n\nXml to Tsv conversion done successfully.")

    
