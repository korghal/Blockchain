import hashlib
import requests

import sys


# TODO: Implement functionality to search for a proof 
def proof_of_work(last_proof):
        """
        Simple Proof of Work Algorithm
        Find a number p such that hash(last_block_string, p) contains 6 leading
        zeroes
        """
        proof = 0
        proof_found = False
        while not proof_found:
            guess = f'{last_proof}{proof}'.encode()
            guess_hash = hashlib.sha256(guess).hexdigest()
            leadSequence = guess_hash[0:6]
            if leadSequence == '000000':
                proof_found = True
                return proof
            else:
                proof_found = False
                proof += 1


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and look for a new one
        print(f'Requesting last proof from {node}/last-proof')
        req = requests.get(f'{node}/last-proof')
        print(req.json()["last_proof"])
        last_proof = req.json()["last_proof"]

        proof = proof_of_work(last_proof)
        print(proof)

        # TODO: When found, POST it to the server {"proof": new_proof}
        mine_post = requests.post(f'{node}/mine', json={"proof": f'{proof}'})
        print(mine_post.json())

        # TODO: If the server responds with 'New Block Forged'
        if mine_post.json()['message'] == 'New Block Forged':
            coins_mined += 1
            print(f'You now have: {coins_mined} coins!')
        else:
            print(mine_post.json()['message'])
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        pass
