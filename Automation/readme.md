## Instructions
### This folder should be downloaded to your local computer in order to start establishing the whole system.
### Requirements:
boto 2.48
ansible 2.5
### Arguments
<server_type>: [harvester|analyser|database]
harvester: machine crawling data from twitter
analyser: classify and analyse data
database: provide couchDB service and the website.

### Start Command
sh ./start.sh <server_type>
