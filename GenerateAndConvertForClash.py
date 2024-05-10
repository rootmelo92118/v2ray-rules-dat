import os, sys

def dataProcesser(domain_datas):
    exportData = ""
    domainNum = 0
    fullNum = 0
    keywordNum = 0
    regexpNum = 0
    for domainData in domain_datas:
        if "domain" == domainData[0]:
            exportData = exportData + "  - DOMAIN-SUFFIX," + domainData[1] + "\n"
            domainNum += 1
        elif "full" == domainData[0]:
            exportData = exportData + "  - DOMAIN," + domainData[1] + "\n"
            fullNum += 1
        elif "keywod" == domainData[0]:
            exportData = exportData + "  - DOMAIN-KEYWORD," + domainData[1] + "\n"
            keywordNum += 1
        elif "regexp" == domainData[0]:
            regexpNum += 1
    exportData = exportData.strip("\n")
    return [exportData,domainNum,fullNum,keywordNum,regexpNum]

def main(source="./data", output="./clash_Rule_Set"):
    sourceDir = os.listdir(source)
    exportList = ""
    for i in range(0,len(sourceDir)):
        if i == len(sourceDir)-1:
            exportList = exportList + sourceDir[i]
        else:
            exportList = exportList + sourceDir[i] + ","
    os.system("go run ./ --outputpath=" + output + " --exportlists=" + exportList)
    print("\n\n")
    for i in sourceDir:
        i = i.lower()
        with open(output + "/" + i + ".txt","r") as f:
            rawData = f.readlines()
            f.close()
        processingData = []
        for rawDomain in rawData:
            processingData.append(rawDomain.strip("\n").split(":"))
        exportData = dataProcesser(processingData)
        description = "# Source: https://github.com/v2fly/domain-list-community/blob/master/data/" + i + "\n" + "# domain: " + str(exportData[1]) + "\n" + "# full: " + str(exportData[2]) + "\n" + "# keyword: " + str(exportData[3]) + "\n" + "# regexp: " + str(exportData[4]) + " (not in rule-set)\n\n\npayload:\n"
        with open(output + "/" + i + ".yaml","w") as f:
            f.write(description + exportData[0])
            f.close()
        print(i + " has been converted.")
        os.remove(output + "/" + i + ".txt")
    print("All jobs have been done successfully.")

    

if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2])
