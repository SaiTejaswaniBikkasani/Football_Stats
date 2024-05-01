from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime
import pandas as pd
import time

# To access the team name from the user.
league_name = input()
league_name = league_name.title()

country_name1 = input()
country_name2 = input()

# To get the today date in the form dd/mm/yy.
today = datetime.today()
formatted_date = today.strftime("%d/%m/%y")
formatted_date_datetime = datetime.strptime(formatted_date, "%d/%m/%y")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://fcstats.com")
# time.sleep(40)
tog = driver.find_element(By.ID, "leaguesToggleLink")
# Click the element
tog.click()

# Find all elements with the specified class
elements = driver.find_elements(By.CLASS_NAME, "menuCountry")

# Iterate through each element and check the text content
for element in elements:
    country_name = element.text.strip()
    if country_name == league_name:  # Change this to the desired country name
        element.click()
        break  # Stop iterating if the desired country is found

time.sleep(10)
header_element = driver.find_element(By.TAG_NAME, "h1")
header_text = header_element.text.split("-")
required_league = header_text[0].strip() + ": " + header_text[-1].strip()
required_league_name = required_league + " - Regular season"

table = driver.find_element(By.XPATH, "//a[text()='Table']")
table.click()

#time.sleep(40)

home_team_names = []
away_team_names = []
league_dates = []
league_points = []


def leagues_info(country_name, years_list, leagues_list):
    teams = driver.find_elements(By.CSS_SELECTOR, ".teamName")
    time.sleep(10)
    team_names = [team.text for team in teams]

    for name in team_names:
        if name == country_name:
            country_button = driver.find_element(By.XPATH, f"//a[text()='{name}']")
            country_button.click()
            time.sleep(10)
            break

    for i in range(len(years_list)):
        years_dropdown = driver.find_element(By.CLASS_NAME, "league_select_year")
        years_dropdown.click()
        time.sleep(7)
        options = years_dropdown.find_elements(By.TAG_NAME, "option")

        year_found = False

        # Loop through the options and select the one that matches the target year
        for option in options:
            if option.text.strip() == years_list[i]:
                option.click()
                year_found = True
                break

        time.sleep(7)

        if not year_found:
            continue

        leagues_dropdown = driver.find_element(By.ID, value=f"season_{leagues_list[i]}")
        leagues_dropdown.click()
        time.sleep(8)
        leagues = driver.find_elements(By.CSS_SELECTOR, ".league_select_phase option")

        league_found = False

        # Loop through the leagues and select the one that matches the target league
        for league in leagues:
            if league.text.strip() == required_league_name:
                league.click()
                league_found = True
                break
        time.sleep(10)

        # for league in leagues[::-1]:
        #     try:
        #         league.click()
        #         league_found = True
        #         break  # Break the loop once clicked
        #     except Exception as e:
        #         print(f"Error clicking league: {e}")

        time.sleep(10)

        if not league_found:
            # Handle the case where the expected league is not found.
            print(f"Warning: Expected league not found for {years_list[i]} of the team {country_name}")
        else:
            # To click on the matches button.
            time.sleep(5)
            matches = driver.find_element(By.XPATH, "//a[text()='Matches']")
            matches.click()
            time.sleep(10)

            # It gives the list of team homes.
            teamHomes = driver.find_elements(By.CSS_SELECTOR, ".teamHomeName")
            time.sleep(10)
            teamHomeNames = [name.text for name in teamHomes if name.text != '']
            home_team_names.extend(teamHomeNames)

            # It gives the list of teams away from home.
            teamAway = driver.find_elements(By.CSS_SELECTOR, ".teamAwayName")
            time.sleep(10)
            teamAwayNames = [name.text for name in teamAway if name.text != '']
            away_team_names.extend(teamAwayNames)

            # It gives all the leagues dates.
            all_dates = driver.find_elements(By.CSS_SELECTOR, ".matchDate")
            time.sleep(10)
            non_empty_dates = [date.text for date in all_dates if date.text.strip()]
            dates = [datetime.strptime(date, "%d/%m/%y") for date in non_empty_dates]
            filtered_dates = [date.strftime("%d/%m/%y") for date in dates if date <= formatted_date_datetime]
            league_dates.extend(filtered_dates)

            # It gives the score between the teams.
            all_points = driver.find_elements(By.CSS_SELECTOR, ".matchResult")
            time.sleep(10)
            points = [point.text for point in all_points if point.text.strip()]
            league_points.extend(points)


years_list = ["2022/2023", "2023/2024", "2022", "2023", "2024"]
leagues_list = ["20222023", "20232024", "20222022", "20232023", "20242024"]
leagues_info(country_name1, years_list, leagues_list)
driver.close()
time.sleep(40)

# To get the lists of same length to create dataframe.
min_length = min(len(league_dates), len(home_team_names), len(away_team_names), len(league_points))
home_team_names = home_team_names[:min_length]
away_team_names = away_team_names[:min_length]
league_dates = league_dates[:min_length]
league_points = league_points[:min_length]


# Creating a DataFrame.
data = {
    'Date': league_dates,
    'Home Team': home_team_names,
    'Points': league_points,
    'Away Team': away_team_names
}
df = pd.DataFrame(data)

# Writing the data to Excel.
# writer = pd.ExcelWriter(f"{country_name1}.xlsx", engine='xlsxwriter')
# df.to_excel(writer, index=False)
# writer.close()
df.to_excel(f'{country_name1}.xlsx', index=False)

league_dates = []
home_team_names = []
away_team_names = []
league_points = []

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://fcstats.com")
tog = driver.find_element(By.ID, "leaguesToggleLink")
# Click the element
tog.click()

# Find all elements with the specified class
elements = driver.find_elements(By.CLASS_NAME, "menuCountry")

# Iterate through each element and check the text content
for element in elements:
    country_name = element.text.strip()
    if country_name == league_name:  # Change this to the desired country name
        element.click()
        break  # Stop iterating if the desired country is found

table = driver.find_element(By.XPATH, "//a[text()='Table']")
table.click()

leagues_info(country_name2, years_list, leagues_list)

# To get the lists of same length to create dataframe.
min_length = min(len(league_dates), len(home_team_names), len(away_team_names), len(league_points))
home_team_names = home_team_names[:min_length]
away_team_names = away_team_names[:min_length]
league_dates = league_dates[:min_length]
league_points = league_points[:min_length]


# Creating a DataFrame.
data = {
    'Date': league_dates,
    'Home Team': home_team_names,
    'Points': league_points,
    'Away Team': away_team_names
}
df = pd.DataFrame(data)

# Writing the data to Excel.
# writer = pd.ExcelWriter(f"{country_name2}.xlsx", engine='xlsxwriter')
# df.to_excel(writer, index=False)
# writer.close()
df.to_excel(f'{country_name2}.xlsx', index=False)
time.sleep(10)

driver.close()

time.sleep(10)

country1 = pd.read_excel(f"{country_name1}.xlsx")
country2 = pd.read_excel(f"{country_name2}.xlsx")
# country1 = pd.read_excel(f"{country_name1}.xlsx")
# country2 = pd.read_excel(f"{country_name2}.xlsx")
# To convert them into required format.
country2.Date = pd.to_datetime(country2.Date)
country1.Date = pd.to_datetime(country1.Date)
country2["Home Team"] = country2["Home Team"].astype(str)
country1["Home Team"] = country1["Home Team"].astype(str)
country2["Away Team"] = country2["Away Team"].astype(str)
country1["Away Team"] = country1["Away Team"].astype(str)

result = country2[country2["Home Team"].str.split(" ").str[-1] == country_name2.split(" ")[-1]]
result1 = country2[country2["Away Team"].str.split(" ").str[0] == country_name2.split(" ")[0]]


unique_away_teams = result["Away Team"].unique()
filtered_country1 = country1[country1["Away Team"].isin(unique_away_teams)]
comparison = filtered_country1[(filtered_country1["Home Team"].str.split(" ").str[-1] == country_name1.split(" ")[-1]) &
                                   (filtered_country1["Away Team"].isin(unique_away_teams))]

unique_away_teams_result1 = result1["Home Team"].unique()
filtered_country1_result1 = country1[country1["Home Team"].isin(unique_away_teams_result1)]
comparison_result1 = filtered_country1_result1[(filtered_country1_result1["Away Team"].str.split(" ").str[0] == country_name1.split(" ")[0]) &
                                                     (filtered_country1_result1["Home Team"].isin(unique_away_teams_result1))]

comparison["Year"] = pd.to_datetime(comparison["Date"]).dt.year
result["Year"] = pd.to_datetime(result["Date"]).dt.year

merged_comparison1 = pd.merge(comparison, result, on=["Away Team", "Year"], how="inner")

merged_comparison1 = merged_comparison1.drop("Year", axis=1)

comparison_result1["Year"] = pd.to_datetime(comparison_result1["Date"]).dt.year
result1["Year"] = pd.to_datetime(result1["Date"]).dt.year

merged_comparison2 = pd.merge(comparison_result1, result1, on=["Home Team", "Year"], how="inner")

merged_comparison2 = merged_comparison2.drop("Year", axis=1)

data1 = {
    "Date": merged_comparison1.Date_x,
    "Home Team": merged_comparison1["Home Team_x"],
    "Points": merged_comparison1["Points_x"],
    "Away Team": merged_comparison1["Away Team"],
}

df = pd.DataFrame(data1)

data2 = {
    "Dates": merged_comparison1.Date_y,
    "Home Team": merged_comparison1["Home Team_y"],
    "Points": merged_comparison1["Points_y"],
    "Away Team": merged_comparison1["Away Team"],
}

df1 = pd.DataFrame(data2)

data3 = {
    "Date": merged_comparison2.Date_x,
    "Home Team": merged_comparison2["Home Team"],
    "Points": merged_comparison2["Points_x"],
    "Away Team": merged_comparison2["Away Team_x"],
}

df2 = pd.DataFrame(data3)

data4 = {
    "Dates": merged_comparison2.Date_y,
    "Home Team": merged_comparison2["Home Team"],
    "Points": merged_comparison2["Points_y"],
    "Away Team": merged_comparison2["Away Team_y"],
}

df3 = pd.DataFrame(data4)

# To concatenate the two DataFrames.
combined_df = pd.concat([df, df2], ignore_index=True)

combined_df1 = pd.concat([df1, df3], ignore_index=True)

# The final dataframe:
combined_final = pd.concat([combined_df, combined_df1], axis=1)

combined_final['Year'] = pd.to_datetime(combined_final['Date'], format='%d/%m/%y').dt.year

# Sorting the DataFrame by the 'Year' and 'Date' columns
combined_final.sort_values(['Year', 'Date'], inplace=True)
combined_final.drop('Year', axis=1, inplace=True)


# Format the 'Date' column to 'd/m/y' format
combined_final['Date'] = combined_final['Date'].dt.strftime('%d/%m/%y')
combined_final['Dates'] = combined_final['Dates'].dt.strftime('%d/%m/%y')

combined_final.to_excel("combined_data.xlsx", index=False)
# writer = pd.ExcelWriter(f"combined_data.xlsx", engine='xlsxwriter')
# combined_final.to_excel(writer, index=False)
# writer.close()

df1 = pd.read_excel(f"{country_name1}.xlsx")
df2 = pd.read_excel(f"{country_name2}.xlsx")
# df1 = pd.read_excel(f"{country_name1}.xlsx")
# df2 = pd.read_excel(f"{country_name2}.xlsx")
team1 = "".join(filter(str.isalpha, country_name1))
team2 = "".join(filter(str.isalpha, country_name2))


def points_table(team,  dataf):
    opponent_matches = {}

    # Group matches by opponent
    for index, row in dataf.iterrows():
        date = row['Date']
        home_team = ''.join(filter(str.isalpha, row['Home Team']))  # Removing numerical parts
        points_str = row['Points']
        if ':' not in points_str:
            continue  # Skip this row if 'Points' does not contain ':'
        home_points, away_points = points_str.split(':')
        away_team = ''.join(filter(str.isalpha, row['Away Team']))  # Removing numerical parts
        opponent = home_team if home_team != team else away_team
        if opponent not in opponent_matches:
            opponent_matches[opponent] = []
        opponent_matches[opponent].append((date, home_team, int(home_points), away_team, int(away_points)))

    # Create DataFrame for the reorganized data
    data = []
    for opponent, matches in opponent_matches.items():
        row = {f"{team} Opponent": opponent}
        for i in range(4):
            if i < len(matches):
                date, home_team, home_points, away_team, away_points = matches[i]
                row[f"Match {i+1} Date"] = date
                row[f"Match {i+1} {team} Points"] = home_points if home_team == team else away_points
                row[f"Match {i+1} Opponent Points"] = away_points if home_team == team else home_points
            else:
                row[f"Match {i+1} Date"] = ""
                row[f"Match {i+1} {team} Points"] = ""
                row[f"Match {i+1} Opponent Points"] = ""
        data.append(row)

    # Create DataFrame for the reorganized data
    reorganized_df = pd.DataFrame(data)

    # Save DataFrame to Excel
    reorganized_df.to_excel(f"{team}new.xlsx", index=False)
    # writer = pd.ExcelWriter(f"{team}new.xlsx", engine='xlsxwriter')
    # reorganized_df.to_excel(writer, index=False)
    # writer.close()
    time.sleep(10)


points_table(team1, df1)
time.sleep(10)
points_table(team2, df2)
time.sleep(5)

reorganized_df1 = pd.read_excel(f"{team1}new.xlsx")
reorganized_df2 = pd.read_excel(f"{team2}new.xlsx")
# reorganized_df1 = pd.read_excel(f"{team1}new.xlsx")
# reorganized_df2 = pd.read_excel(f"{team2}new.xlsx")
# Merging the two dataframes based on the opponents.
merged_df = pd.merge(reorganized_df1, reorganized_df2, left_on=f"{team1} Opponent", right_on=f"{team2} Opponent", how="outer")

merged_df.fillna("", inplace=True)

merged_df.to_excel("merged_data.xlsx", index=False)
# writer = pd.ExcelWriter(f"merged_data.xlsx", engine='xlsxwriter')
# merged_df.to_excel(writer, index=False)
# writer.close()
