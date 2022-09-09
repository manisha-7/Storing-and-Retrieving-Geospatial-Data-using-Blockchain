from Blockchain import block_chain as blockchain
from datetime import date

def add_block(Coordinate, date, Location, Satellite, type_of_data, ipfshash, viewusers,userkanaam):
    data = {
        'coordinate' : Coordinate,
        'date' : date,
        'place' : Location,
        'satellite' : Satellite,
        'datatype' : type_of_data,
        'ipfs_hash' : ipfshash,
        'viewusers' : viewusers,
        'userkanaam': userkanaam
    }
    previous_block = len(blockchain.blockchain.chain)-1
    previous_hash = blockchain.blockchain.hashh(previous_block)
    block = blockchain.blockchain.check_presence(previous_hash, data, userkanaam)

def validate():
    valid = blockchain.blockchain.chain_valid(blockchain.blockchain.chain)
    print(valid)
    
def disp():
    print(blockchain.blockchain.chain)
    
def extractdata(coordinate, startdate, enddate, location, datatype, satellite):
    return (blockchain.blockchain.extract_data(coordinate, startdate, enddate, location, datatype, satellite))


def modify_per(val):
    return (blockchain.blockchain.modify_perm(val))

def makechange(val, addp, rp):
    blockchain.blockchain.macc(val, addp, rp)
