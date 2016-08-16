import settings
from collectLinks import soupTheLink
def compileData(listOfShowLinks):
    
    shows = [url[2:-2] for url in listOfShowLinks]
    settings.DATABASE['title'].extend(shows)
    
    for url in listOfShowLinks[:5]:
        
        souped = collectLinks.soupTheLink(url)
        
        for table in souped.find_all(class_='infobox'):
            for row in table.find_all('tr'):
                for info in row.find_all('td'):
                    rowContent = info.contents

                    if rowContent == 'Genre':

                        try:
                            settings.DATABASE['genre'].append(rowContent)
                        except IndexError:
                            settings.DATABASE['genre'].append("NA")

                    elif rowContent == 'Created by':

                        try:
                            settings.DATABASE['created_by'].append(rowContent)
                        except IndexError:
                            settings.DATABASE['created_by'].append("NA")

                    elif rowContent == 'Starring':

                        try:
                            settings.DATABASE['starring'].append(rowContent)
                        except IndexError:
                            settings.DATABASE['starring'].append("NA")

                    elif rowContent == 'Network':

                        try:
                            settings.DATABASE['network'].append(rowContent)
                        except IndexError:
                            settings.DATABASE['network'].append("NA")

                    elif rowContent == 'Original release':

                        try:
                            settings.DATABASE['release'].append(rowContent)
                        except IndexError:
                            settings.DATABASE['release'].append("NA")

                    elif rowContent == 'seasons':

                        try:
                            settings.DATABASE['num_seasons'].append(rowContent)
                        except IndexError:
                            settings.DATABASE['num_seasons'].append("NA")

                    elif rowContent == 'episodes':

                        try:
                            settings.DATABASE['num_episodes'].append(rowContent)
                        except IndexError:
                            settings.DATABASE['num_episodes'].append("NA")

                    else:
                        continue

