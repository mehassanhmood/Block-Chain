# Importing the necessary libraries and dependencies :
import streamlit as st
import pandas as pd
from dataclasses import dataclass
from typing import Any, List
import datetime as dt
import hashlib
# making the record dataclass :
@dataclass
class Record:
    sender : str
    receiver : str
    amount : float
# making the block dataclass
@dataclass
class Block:
    record : Record
    creator_id : int
    prev_hash : str = '0'
    timestamp : str = dt.datetime.utcnow().strftime('%H:%M:%S')
    nonce : int = 0
    
    def hash_block(self):
        sha = hashlib.sha256()
        
        record = str(self.record).encode()
        sha.update(record)
        
        creator_id = str(self.creator_id).encode()
        sha.update(creator_id)
        
        prev_hash = str(self.prev_hash).encode()
        sha.update(prev_hash)
        
        timestamp = str(self.timestamp).encode()
        sha.update(timestamp)
        
        nonce = str(self.nonce).encode()
        sha.update(nonce)
        
        return sha.hexdigest()
# making the PyChain class:
@dataclass
class PyChain:
    chain: List[Block]
    difficulty: int =4
    
    def proof_of_work(self,block):
        calculated_hash = block.hash_block()
        number_of_zeros = '0'*self.difficulty
        
        while not calculated_hash.startswith(number_of_zeros):
            block.nonce += 1
            calculated_hash = block.hash_block()
            
        print('winning hash :' , calculated_hash)
        return block
    
    def add_block(self,candidate_block):
        block = self.proof_of_work(candidate_block)
        self.chain += [block]
        
    def is_valid(self):
        block_hash = self.chain[0].hash_block()
        
        for i in self.chain[1:]:
            if block_hash != i.prev_hash:
                print('Block cain is invalid')
                return False
            block_hash = i.hash_block()
            print('Block chain is valid')
            return True
            # Streamlit code:
@st.cache(allow_output_mutation = True)
def setup():
    return PyChain([Block('Genesis',0)])
st.markdown('# PyChain')
st.markdown('## Store a transaction Record in PyChain')
pychain = setup()

Record.sender = st.text_input('Sender')
Record.receiver =st.text_input('Receiver')
Record.amount = st.text_input('Amount')

if st.button('Add Block'):
    prev_block  = pychain.chain[-1]
    prev_block_hash = prev_block.hash_block()
    
    new_block = Block(record = Record,
                      creator_id = 42,
                      prev_hash = prev_block_hash)
    
    pychain.add_block(new_block)
    st.balloons()
    
st.markdown('### The PyChain Ledger')
pychain_df = pd.DataFrame(pychain.chain).astype(str)
st.write(pychain_df)

difficulty = st.sidebar.slider('Block Difficulty',1,5,2)
pychain.difficulty = difficulty

st.sidebar.write('#Block Inspector')
selected_block = st.sidebar.selectbox('Which block would you like to see ?' ,pychain.chain)
st.sidebar.write(selected_block)

if st.button('validate chain'):
    st.write(pychain.is_valid())