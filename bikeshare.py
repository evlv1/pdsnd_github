import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
def quit_funct(leave):
    """Allows the user to quit the script with the keyword 'exit'. """
    if leave == 'exit':
        print("Bye Bye!")
        quit()


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    cities =('chicago', 'new york city', 'washington')
    city =''
    while not (city in cities or city=='exit'):
        city= input("Please select a city: Chicago, New York City, Washington. Type 'Exit' to leave.\n").lower()
        quit_funct(city)
        if not city in cities: print("Oops, there must be a typo in your input. Please try again.\n")

    months=('all','january', 'february', 'march', 'april', 'may', 'june')
    month=""
    while not (month in months or month=='exit'):
        month= input("Now lets select a month. The data for January, February, March, April, May and June is availible.\nType \'all\' if you don\'t want to filter for a month. Type \'Exit\' to leave.\n").lower()
        quit_funct(month)
        if not month in months: print("Oops, there must be a typo in your input. Please try again.\n")

    days=('all','mo', 'tu', 'we', 'th', 'fr', 'sa', 'su')
    day=""
    while not (day in days or day=='exit'):
        day= input("Finally, please select a weekday. Please enter as Mo, Tu, We, Th, Fr, Sa or Su.\nType 'all' if you don't want to filter for a day. Type 'Exit' to leave.\n").lower()
        quit_funct(day)
        if not day in days: print("Oops, there must be a typo in your input. Please try again.\n")

    print("Your statsics will be calculated for:")
    print("CITY: "+city.title())
    print("MONTH: "+month.title())
    print("DAY: "+day.title())
    confirm =""
    while not (confirm == "y" or confirm == "n"):
        confirm=input("Please confirm your selection. Enter \'y\' to continue or \'n\' restart the selection: ").lower()
    if confirm == "n":
        get_filters()

    print('-'*84)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    CITY_DATA = { 'chicago': 'chicago.csv',
                  'new york city': 'new_york_city.csv',
                  'washington': 'washington.csv' }


    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        days = ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'su']
        day = days.index(day)
        df = df[df['day_of_week'] == day]

    return df



def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel.
    If month and/or weekday are used as filters, they are not calculated for stistics."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    if month == 'all':
        rev_month_list =['January', 'February', 'March', 'April', 'May', 'June']
        rev_month=rev_month_list[df['Start Time'].dt.month.mode()[0]-1]
        print("The most common month of travel was {}".format(rev_month))
    else:
        print("In the selected month {}".format(month.title()))

    if day == 'all':
        rev_days_list =['Mo', 'Tu', 'We', 'Thu', 'Fr', 'Sa', 'Su']
        rev_day=rev_days_list[df['Start Time'].dt.weekday.mode()[0]]
        print("The most common weekday of travel was {}".format(rev_day))
    else:
        print("On the selected weekday {}".format(day.title()))

    print("The most common start hour was the hour "+str(df['Start Time'].dt.hour.mode()[0]))

    print("\nThese calculations took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print("The most common start station was \'"+str(df['Start Station'].mode()[0])+"\'")
    print("The most common end station was \'"+str(df['End Station'].mode()[0])+"\'")
    df['Start-End'] =("\'" + df['Start Station'] + "\' as start station with \'" + df['End Station'] + "\' as end station")
    print("The most frequent start - end station combination was " + df['Start-End'].mode()[0])

    print("\nThese calculations took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print("Total trevel time was "+str(df['Trip Duration'].sum())+ " seconds ("+str(pd.to_timedelta(df['Trip Duration'].sum().round(decimals=0), unit='s'))+")")
    print("Mean trevel time was "+str(int(df['Trip Duration'].mean().round(decimals=0)))+ " seconds ("+str(pd.to_timedelta(df['Trip Duration'].mean().round(decimals=0), unit='s'))+")")

    print("\nThese calculations took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    print("The distribution of user types was as follows:")
    print(str(df['User Type'].value_counts(dropna=False))+"\n")

    # Additionally, average trip duration and mots common start - end station combination per user type are shown
    td_s=df['Trip Duration'].groupby(df['User Type']).mean().round(decimals=0).astype('int64')

    print("The mean trip duration of each user type in seconds was:\n{}".format(str(td_s)))
    print("\nThe most common start - end station combinations per use type were:")
    for i in df['User Type'].dropna().unique():
        print("\n"+str(i)+":\n"+str(df['Start-End'].groupby(df['User Type']==i).value_counts().head(1)[0]))
    print("")


    if city == 'new york city' or city == "chicago":
        print("The distribution of user genders was as follows:")
        print(str(df['Gender'].value_counts(dropna=False))+"\n")
        print("The erliest year of birth was "+str(int(df['Birth Year'].min())))
        print("The most recent year of birth was "+str(int(df['Birth Year'].max())))
        print("The emost common year of birth was "+str(int(df['Birth Year'].mode()[0])))

    print("\nThese claculations took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data (df):
    """Displays original raw data from the csv files in 5-line-steps."""

    raw_user_inp= input("Do you want to see original raw data? Enter 'y' to start. Type \'Exit\' to leave: ").lower()
    quit_funct(raw_user_inp)

    if raw_user_inp =='y':
        pd.set_option("display.width", 0)
        s=0
        e=5
        while raw_user_inp =='y' and s < df.shape[0]:
            print(df.iloc[s:e,:-3])
            s+=5
            if e+5 >= df.shape[0]: e=df.shape[0]
            else: e+=5
            raw_user_inp= input("Do you want to see the next 5 lines of raw data? Enter 'y' to continue: ")

    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input("\nWould you like to restart? Enter 'y' to restart .\n")
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
