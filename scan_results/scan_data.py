import re
from scancode import cli
import os

def main():
    if os.path.exists(os.path.join(os.getcwd(), "scrapeData", "data_github")):
        result = cli.run_scan(os.path.join(os.getcwd(), "scrapeData", "data_github"), copyright=True, processes=14, verbose=True, timeout=3600)
        copyrights = []
        for i in result[1]["files"]:
            for j in i["copyrights"]:
                if j["value"] not in copyrights:
                    copyrights.append(j["value"])
        print(copyrights)

if __name__ == "__main__":
    main()