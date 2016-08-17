import pandas as pd
import settings
import collectLinks

def compileData(listOfShowLinks):
    
    shows = [url[30:] for url in listOfShowLinks[:5]]
    settings.DATABASE['title'].extend(shows)
    
    for url in listOfShowLinks[:5]:
        
        souped = collectLinks.soupTheLink(url)
            
        for table in souped.find_all(class_='infobox'):
             
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
                    print('feature = ', feature)

                    if feature == ['Genre']:
                        has_genre = 1
                        
                        rowContent = []
                        
                        for info in row.find_all('td'):
                            for genre in info.find_all('a'):
                                rowContent.extend(genre.contents)
                        print('Genre: ', rowContent)

                        settings.DATABASE['genre'].append(rowContent)

                    elif feature == ['Created by'] or feature == ['Written by']:
                        has_created_by = 1
                        
                        rowContent = []

                        for info in row.find_all('td'):
                            creators = []

                            if len(info) == 1:
                                creators.extend(info.contents)
                            else:
                                for creator in info.find_all('a'):
                                    name = str(creator.contents)
                                    if name[2] != '[':
                                        creators.extend(creator.contents)
                            rowContent.extend(creators)
                        print('Created by: ', rowContent)

                        settings.DATABASE['created_by'].append(rowContent)

                    elif feature == ['Starring']:
                        has_starring = 1
                        
                        rowContent = []

                        for info in row.find_all('td'):
                            
                            if len(info) == 1:
                                rowContent.extend(info.contents)
                                
                            else:
                                for stars in info.find_all('a'):
                                    rowContent.extend(stars.contents)
                            
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

                    elif feature == ['Original release']:
                        has_release = 1

                        for info in row.find_all('td'):
                            rowContent = info.contents
                            print('Original release: ', rowContent)
                            
                            if type(rowContent[0]) != str:
                                rowContent = rowContent[2]
                            else:
                                rowContent = rowContent[0]
                                                                
                            settings.DATABASE['release'].append(rowContent)
                    
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
                            print('seasons: ', rowContent)
                            
                            settings.DATABASE['num_seasons'].append(rowContent)

                    elif feature[-1] == ' of episodes':
                        has_num_episodes = 1

                        for info in row.find_all('td'):
                            rowContent = info.contents[0]
                            print('episodes:', rowContent)
                            settings.DATABASE['num_episodes'].append(rowContent)
                            

                    else:
                        continue

            if has_genre == 0:
                settings.DATABASE['genre'].append("None")
            if has_created_by == 0:
                settings.DATABASE['created_by'].append("None")
            if has_starring == 0:
                settings.DATABASE['starring'].append("None")
            if has_network == 0:
                settings.DATABASE['network'].append("None")
            if has_release == 0:
                settings.DATABASE['release'].append("None")
            if has_running_time == 0:
                settings.DATABASE['running_time'].append("None")
            if has_num_seasons == 0:
                settings.DATABASE['num_seasons'].append("None")
            if has_num_episodes == 0:
                settings.DATABASE['num_episodes'].append("None")

def main():
    mainUrl = 'https://en.wikipedia.org/wiki/List_of_American_television_series'
    links = collectLinks.collectLinks(mainUrl)
    compileData(links)
    TABLE_COLUMNS = ['title', 'genre', 'created_by', 'starring', 'network', 'release', 'running_time', 'num_seasons', 'num_episodes']
    df = pd.DataFrame(settings.DATABASE, columns = settings.TABLE_COLUMNS)
    
    print(df.head())
    df.to_csv(settings.TABLE_NAME)

if __name__ == "__main__":
    main()