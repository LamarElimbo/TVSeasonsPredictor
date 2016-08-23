import pandas as pd
import settings
import collectLinks
import os
import csv

def compileData(listOfShowLinks):
    print("number of shows = ", len(listOfShowLinks))
    count = 0
    print(listOfShowLinks)
    for url in listOfShowLinks[2237:]:
        count += 1
        print('show number ', count)
        souped = collectLinks.soupTheLink(url[0])

        table_num = 0
        for table in souped.find_all(class_='infobox'):
            table_num += 1
            if table_num == 1:
                has_genre = 0
                has_created_by = 0
                has_starring = 0
                has_network = 0
                has_release = 0
                has_running_time = 0
                has_num_seasons = 0
                has_num_episodes = 0

                for row in table.find_all('tr'):

                    for category in row.find_all('th'):
                        feature = category.contents

                        if feature == ['Genre']:
                            has_genre = 1

                            rowContent = []

                            for info in row.find_all('td'):
                                for genre in info.find_all('a'):
                                    rowContent.extend(genre.contents)
                            print('Genre: ', rowContent)

                            if rowContent == []:
                                for info in row.find_all('td'):
                                    rowContent.extend(info.contents)
                                print('Genre: ', rowContent)

                            settings.DATABASE['genre'].append(rowContent)

                        elif feature == ['Created by'] or feature == ['Written by'] and has_created_by == 0:
                            has_created_by = 1

                            rowContent = []

                            for info in row.find_all('td'):
                                creators = []

                                for creator in info.find_all('a'):
                                    name = str(creator.contents)
                                    if name[2] != '[':
                                        creators.extend(creator.contents)
                                rowContent.extend(creators)
                            print('Created by: ', rowContent)

                            if rowContent == []:
                                for info in row.find_all('td'):
                                    rowContent.extend(info.contents)
                                rowContent = rowContent[0]
                                print('Created by: ', rowContent)

                            settings.DATABASE['created_by'].append(rowContent)

                        elif feature == ['Starring']:
                            has_starring = 1

                            rowContent = []

                            for info in row.find_all('td'):

                                for stars in info.find_all('a'):
                                    rowContent.extend(stars.contents)

                            print('Starring: ', rowContent)

                            if rowContent == []:
                                for info in row.find_all('td'):
                                    rowContent.extend(info.contents)
                                rowContent = rowContent[0]
                                print('Starring: ', rowContent)

                            settings.DATABASE['starring'].append(rowContent)

                        elif feature == ['Original network']:
                            has_network = 1

                            rowContent = []

                            for info in row.find_all('td'):
                                for network in info.find_all('a'):
                                    rowContent.extend(network.contents)
                            print('Network: ', rowContent)

                            settings.DATABASE['network'].append(rowContent)

                        elif feature == ['Running time']:
                            has_running_time = 1

                            rowContent = []

                            for info in row.find_all('td'):
                                rowContent = info.contents
                                print('Running time: ', rowContent)

                                rowContent = rowContent[0]
                                rowContent = rowContent[0:2]

                                settings.DATABASE['running_time'].append(rowContent)

                        elif feature[-1] == ' of seasons':
                            has_num_seasons = 1

                            for info in row.find_all('td'):
                                rowContent = info.contents[0]
                                print('Seasons: ', rowContent)

                                settings.DATABASE['num_seasons'].append(rowContent)

                        elif feature[-1] == ' of episodes':
                            has_num_episodes = 1

                            for info in row.find_all('td'):
                                rowContent = info.contents[0]
                                print('Episodes:', rowContent)
                                settings.DATABASE['num_episodes'].append(rowContent)


                        else:
                            continue
                    
                if has_genre == 0:
                    print('Genre: None')
                    settings.DATABASE['genre'].append("None")
                if has_created_by == 0:
                    print('Created by: None')
                    settings.DATABASE['created_by'].append("None")
                if has_starring == 0:
                    print('Starring: None')
                    settings.DATABASE['starring'].append("None")
                if has_network == 0:
                    print('Network: None')
                    settings.DATABASE['network'].append("None")
                if has_running_time == 0:
                    print('Running time: None')
                    settings.DATABASE['running_time'].append("None")
                if has_num_seasons == 0:
                    print('Seasons: None')
                    settings.DATABASE['num_seasons'].append("None")
                if has_num_episodes == 0:
                    print('Episodes: None')
                    settings.DATABASE['num_episodes'].append("None")
                    
        if table_num > 0:
            titleCount = 0
            for title in souped.find_all(class_='firstHeading'):
                for content in title.find_all('i'):
                    titleCount = 1
                    showTitle = content.contents
                    print(showTitle)
                    settings.DATABASE['title'].append(showTitle)
                if titleCount == 0:
                    showTitle = title.contents
                    print(showTitle)
                    settings.DATABASE['title'].append(showTitle)

                    
def main():
    os.chdir('..')
    os.chdir(settings.LINKS_DIR)
    with open(settings.LINKS_FILE) as wiki_links:
        reader = csv.reader(wiki_links)
        links = list(reader)    
    
    compileData(links)
    os.chdir('..')
    os.chdir(settings.DATA_DIR)
    df = pd.DataFrame(settings.DATABASE, columns = settings.TABLE_COLUMNS)
    print(df.head())
    df.to_csv(settings.Z_TABLE_NAME)

if __name__ == "__main__":
    main()