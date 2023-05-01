# SCBugGenerator



*SCBugGenerator* is an Ethereum smart contract bug injection framework, it can inject 20 types of bugs into Solidity smart contract. *SCBugGenerator* is compatible with multiple versions of Solidity (Solidity 0.5.x, 0.6.x, 0.7.x).

Users can use *SCBugGenerator* to generate the large-scale vulnerable contract datasets without preparing contracts in advance (*SCBugGenerator* integrates a contract crawler engine, of course, you can also use your contracts).



##  *Getting Started* 

### How to install dependencies

#### Quick install

We provide a docker container of *SCBugGenerator*. In this docker container, we have installed *SCBugGenerator* and all the dependencies  of *SCBugGenerator* needs to run, and collected 66,208 *real contracts* in this container. You just need to pull the docker image and modify the *userNeeds.json* (by *vim*), and you can use *SCBugGenerator*.

Make sure that docker is installed and the network is good. Enter the following instructions in the terminal (eg., ubuntu os):

```shell
sudo docker pull xf15850673022/huanggai:1.0
sudo docker run -it xf15850673022/huanggai:1.0
root@d3eef7f13492:~/HuangGai# ln -s /usr/bin/python3 /usr/bin/python
```



#### Complete Installation

By following these steps, you can completely install *SCBugGenerator* on your device.

*SCBugGenerator* requires Python 3.6+.

1. Clone source code
```
git clone https://github.com/Our4514444/SCBugGenerator.git
```

##### Note for Artifact Evaluation

It is worth noting that the program we uploaded in Zenodo is no different from the program we open-source on Github. Therefore, you still need to install the dependencies required for *SCBugGenerator*, and make sure that python 3.6+ is installed on your device. If you are just evaluating the functionality of *SCBugGenerator*, then we recommend the docker version of *SCBugGenerator*.

​	2. Install dependencies

*SCBugGenerator* needs to use [Slither](https://github.com/crytic/slither) and [Scrapy](https://github.com/scrapy/scrapy), so please use the following commands to install dependencies:

```
cd SCBugGenerator/
pip install --upgrade pip
pip install rich
pip install graphvi
pip install pydot
pip install slither-analyzer
pip install scrapy
```

3. Install multiple *solc* versions

We use [solc-select](https://github.com/crytic/solc-select) to install multiple versions of solc:
```
cd ..
git clone https://github.com/crytic/solc-select.git
./solc-select/scripts/install.sh
```

This will install `solc` into `~/.solc-select/`, so you have to add it to the **PATH** variable. Add this line, replacing **USERNAME** with your username, to your `.bashrc` or equivalent:
```
export PATH=/home/USERNAME/.solc-select:$PATH
```

## Supported operating systems
At present, we have only tested *SCBugGenerator* on Ubuntu (18.04).

## A small example of how to use *SCBugGenerator*

If you installed *SCBugGenerator* through docker, or you installed *SCBugGenerator* locally and collected the *real contract* (see below for collection method. Or you can use the real contract dataset provided by us [our real contract dataset url](https://github.com/xf97/HuangGai/blob/master/sourceCodeDateSet.zip), you need to download and unzip this dataset, and then move these real contracts into path `src/contractSpider/contractCodeGetter/sourceCode`), then you can verify the functionality of *SCBugGenerator* by doing the following:

### Step 1: specify your needs

*SCBugGenerator* can generate the pecified number of buggy contracts containing different types of bugs according to the user's needs. Therefore, users first need to specify their needs.

Specifically, you need to modify file `/src/userNeeds.json` (in locally installation) or file `userNeeds.json` (in docker installation) to specify the number of buggy contracts that contain each type of bug. File `/src/userNeeds.json` (in locally installation) or file `userNeeds.json` (in docker installation) is a JSON file, and the content structure of this file is as follows:

```json
[bug type]: [the number of contracts you need to contain this type of bug, the time limit for injecting this type of bug (in minutes)]
```

In this example, we recommend that you modify file `/src/userNeeds.json` (in locally installation) or file `userNeeds.json` (in docker installation) to the following:
Set 18 types of bugs except for *re-entrancy bug* and *specify function variable as any type bug* as follows:

```
[bug type]: [1, 20]
```

Set *re-entrancy bug* and *specify function variable as any type bug* as follows:

```
[bug type]: [0, 10]
```

The reason why we don't choose to inject *re-entrancy bug* and *specify function variable as any type bug* is that it takes a long time (probably more than 30 minutes) for *SCBugGenerator* to inject these two types of bugs. If you need *SCBugGenerator* to inject these two types of bugs, please set *re-entrancy bug* and *specify function variable as any type bug* as follows:

```
[bug type]: [1, 60]
```

### Step 2: start injecting

Enter the following commands in the command-line interface to start the injection (eg., ubuntu os):

in locally installation:

```shell
cd src/
ln -s /usr/bin/python3 /usr/bin/python
python3 main.py
```
in  docker installation

```shell
ln -s /usr/bin/python3 /usr/bin/python
python3 main.py
```

And you're done! The injection result will be printed in the  command-line interface.

### Step 3: get buggy contracts

When the injection is completed, *SCBugGenerator* will print the injection result in the command-line interface, including the storage location of the buggy contracts. Specifically, the buggy contract containing each type of bug is stored in path `securityAbandonerAndInjector\BUGTYPE\dataset`, and each buggy contract will have a TXT file describing the locations of the injected bugs (matching by file name).



## How to use (full version)

### Stage 1
First, you need to collect *real contracts* (i.e., smart contracts deployed on Ethereum) before injecting bugs into contracts. *SCBugGenerator* integrates a contract spider (we call this spider *ContractSpider*) developed based on [Python scrapy framework](https://github.com/scrapy/scrapy), which can collect tens of thousands of real contracts in several hours.

Enter the following commands in the terminal (eg., ubuntu os):
```
cd src/contractSpider/contractCodeGetter/data/
python3 autoCrawl.py
```
And you're done! The collected real contracts are stored in the folder `src/contractSpider/contractCodeGetter/sourceCode`.

**Note 1**: the default crawling URL of *ContractSpider* is [cn-etherscan](https://cn.etherscan.com/). We are not sure whether this URL can be accessed in non-China regions. If you encounter problems when collecting real contracts, please try to change the default crawling URL to [etherscan-io](http://etherscan.io/). Specifically, open folder `/src/contractSpider/contractCodeGetter/contractCodeGetter/spiders` and replace all `cn.etherscan.com` in (*codeGetter, getContractAddressSpider, lastContractsAddress, nontokenContractAddress*).py files with `etherscan.io`.

**Note 2**: To reduce the load of the crawled URL, the default crawl interval of *ContractSpider* is 5 seconds per contract. You can reduce or increase the interval by modifying the variable *DOWNLOAD_DELAY* (in seconds) in file `/src/contractSpider/contractCodeGetter/contractCodeGetter/spiders/setting.py`.

**Note 3**: You can also use your contracts (.sol files) by copying them to folder `src/contractSpider/contractCodeGetter/sourceCode`.

**Note 4**: You can also use the *real contract* dataset we collect, which is `sourceCodeDateSet.zip`. After decompressing the `sourceCodeDateSet.zip` (forgive me for my typo (data -> date).), you can get 66,205 *real contracts* and then copy these contracts to folder `src/contractSpider/contractCodeGetter/sourceCode`.

### Stage 2
Make sure that folder `src/contractSpider/contractCodeGetter/sourceCode` contains the *real-world contracts*, and then you can inject bugs into the contracts in the following two steps:
#### Step 1: Specify your needs
Now you should open the file `/src/userNeeds.json` and specify your needs by modifying the content of file `/src/userNeeds.json`. File `/src/userNeeds.json` requires you to specify the number of contracts containing each type of bugs and the maximum injection time.

Specifically, the content structure of file `/src/userNeeds.json` is as follows:
```
[bug type]: [the number of contracts you need to contain this type of bug, the time limit for injecting this type of bug (in minutes)]
```

**Note 5**: Injecting *re-entrancy* and *specify function variable as any type* bugs will take a lot of time. If you need to inject these two types of bugs into the contracts, please specify a longer timeout value.

#### Step 2: Start injecting
Enter the following commands in the terminal to start the injection (eg., ubuntu os):
```
cd src/
python3 main.py
```
And you're done! The injection result will be printed in the terminal.

##  *Detailed Description* 

In our paper, we evaluate *SCBugGenerator* in the following four aspects: **accuracy**, **success rate**, **capture rate** and **speed**（In order to avoid violating the licenses, we only publish the **address names** of the original smart contracts）.

We obtained the **accuracy** of *SCBugGenerator* by manual inspection, which may make our experimental results not easy to obtain. However, we have disclosed the dataset used for evaluation ([dataset for evaluation](https://github.com/Our4514444/SCBugGenerator/tree/main/manualCheckDataset)), which enables researchers to repeat our experimental process and reproduce our experimental results. 

We inject bugs into 1000 smart contracts to obtain **success rate** of *SCBugGenerator* and we have disclosed the dataset used for evaluation. `evaluation/dataset_1000/dataset_1000.xlsx` is the address names of original 1000 smart contracts, `evaluation/dataset_1000/SG` and `evaluation/dataset_1000/SF` are the results of using SG and SF respectively to inject bugs.

We use the current 6 most state-of-the-art smart contract analysis tools to detect bugs injected by *SCBugGenerator*. These six analysis tools (*Maian, Manticore, Mythril, Securify, Slither, SmartCheck*) and the injected contract dataset generated by *SCBugGenerator*  ([dataset for evaluation](https://github.com/Our4514444/SCBugGenerator/tree/main/manualCheckDataset)) are publicly available, which allows users to repeat our experiments.  However, due to the difference in the experimental environment (eg., hardware equipment, operating system, timeout value), this may cause the user to obtain a slightly different **capture rate** from what we claimed in the paper. 

We measure the injection time of *SCBugGenerator* when constructing the evaluation dataset. Users can try to use *SCBugGenerator* to a generate vulnerable contract dataset and measure the running time of *SCBugGenerator* to get the **speed** of *SCBugGenerator*. It is worth noting that different hardware equipment may affect the **speed** of *SCBugGenerator*.



Next, we will introduce the role of *SCBugGenerator*'s various files to help users understand (and improve) our work:



**ContractSpider**

1. contractCodeGetter/scrapy.cfg: The default configuration file in scrapy framework.
2. contractCodeGetter/data/autoCrawl.py: Automatic crawler program, the program will run 4 crawlers one by one and save the crawling results.
3. contractCodeGetter/contractCodeGetter/items.py: The file used to specify the data structure in scrapy framework.
4. contractCodeGetter/contractCodeGetter/middlewares.py: The default middleware file in scrapy framework.
5. contractCodeGetter/contractCodeGetter/pipelines.py: The default pipeline file in scrapy framework, and this file is used to specify the data transmission direction.
6. contractCodeGetter/contractCodeGetter/settings.py: The setting file in scrapy framework, where users can set the crawl interval.
7. contractCodeGetter/contractCodeGetter/spiders/codeGetter.py: The crawler program we create, and this program is used to crawl the contract source code based on the contract address.
8. contractCodeGetter/contractCodeGetter/spiders/getContractAddressSpider.py: The crawler program we create, and this program is used to crawl the addresses of the top 1000 most popular token contracts.
9. contractCodeGetter/contractCodeGetter/spiders/latestContractsAddress.py: The crawler program we create, and this program is used to crawl the addresses of 500 contracts that have been recently open sourced. 
10. contractCodeGetter/contractCodeGetter/spiders/nontokenContractAddress.py: The crawler program we create, and this program is used to crawl the addresses of all open source contracts. 

**ContractExtractor**

 	1. BUGTYPE/BUGTYPExtractor.py: The main program of the *contractExtractor*, and this program is used to prepare the extracted materials and generate the AST and CFG of the contract.
 	2. BUGTYPE/judgePath.py: This program extracts characteristics from the contract‘s CFG.
 	3. BUGTYPE/judgeAst.py: This program extracts characteristics from the contract‘s AST.
 	4. BUGTYPE/inherGraph.py: The program returns the linear inheritance order of the contract, and the most derived contract'name.
 	5. BUGTYPE/colorPrint.py: This program is used to rich text and beautiful formatting in the terminal.
 	6. BUGTYPE/cache: Contracts (and extraction information) that meet the extraction criteria are stored in this folder.

**BugInjector**

1. securityAbandonerAndInjector/BUGTYPE/main.py: The main program of *BugInejctor*, and this program is used to prepare injection materials and run other programs.
2. securityAbandonerAndInjector/BUGTYPE/BUGTYPEInjector.py: The program modifies the contract to inject bugs and labels the locations of injected bugs.
3. securityAbandonerAndInjector/BUGTYPE/dataset:  All injected contracts (and corresponding label files)  are stored in this folder.

**Other files**

1. main.py: *SCBugGenerator* main control program. This program is used to run different types of bug injection modules according to the needs of users.
2. config.json: *SCBugGenerator* default configuration file.
3. userNeeds.json: This file is used to specify needs of users.