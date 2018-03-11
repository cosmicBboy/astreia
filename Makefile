create-conda-env:
	conda create -n astrea-3.6 python=3.6
	conda create -n astrea-2.7 python=2.7

run-eth-server:
	geth --dev --rpc --ipcpath ~/Library/Ethereum/geth.ipc --datadir ~/Library/Ethereum/pyEthTutorial --rpcapi eth,net,web3,personal
