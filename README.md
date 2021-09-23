# linux-logging-2021

- RQ1 contains figures and data to answer RQ1. Refer to ipynb file in https://github.com/iamkeyur/linux-logging-2021/tree/main/RQ1/Figures to create graphs and tables. https://github.com/iamkeyur/linux-logging-2021/blob/main/RQ1/LogDistribution/Final_filtered contains calls extracted from source code.

- RQ2 contains data to answer evolution of logging code. https://github.com/iamkeyur/linux-logging-2021/tree/main/RQ2/Loglevel/1 and https://github.com/iamkeyur/linux-logging-2021/tree/main/RQ2/Loglevel/2 contains changes made to log level. You need to combine data from this two folders. add_final.csv, del_final.csv, and upd_final.csv contains all changes made to loging code. Add it to some database and query it.

- RQ3 contains results from our manual evaluation. https://github.com/iamkeyur/linux-logging-2021/blob/main/RQ3/OutDone contains tag assigned to git comits involved. `awk -F',' '{ for (i=3; i<=NF; i++)   print $i }' OutDone | sort | uniq -c ` can give you summay table.
