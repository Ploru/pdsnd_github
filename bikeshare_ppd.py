import time
import os
import platform
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

cities = ['new york city', 'chicago', 'washington']
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days = ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!'
          '\n'
          'Please select a city to analyze from the below options:'
          '\n'
          'a) New York City'
          '\n'
          'b) Chicago'
          '\n'
          'c) Washington'
          '\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    '''city = str(input('Which City would you like to analyze?:'
                          '\n').lower())'''

    while True:
        city = str(input('Which City would you like to analyze?:'
                                  '\n').lower())
        if city not in cities:
            city = input('Please correct your selection and choose a city from'
                              '\n New York City, Chicago, Washington:'
                              '\n')
            continue
        else:
            break
    print('Perfect! You selected {}, let\'s check for additional filters.'.format(city))
    print()

    # get user input for month (all, january, february, ... , june)
    while True:
        month = str(input('What month would you like to analyze?'\
                                  '\n (select any month from january to june):').lower())
        if month not in months:
            month = input('Please select either a month from january to june (inclusive), or \"all\"'
              '\n for all available months:')
            continue
        else:
            break
        print('Perfect! You selected {}, let\'s check for additional filters.'.format(month))
        print()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str(input('What day of the week would you like to analyze?').title())
        if day not in days:
            day = input('Type in a day of the week (eg: Wednesday) or \"all\":')
            continue
        else:
            break
        print('Perfect! You selected {}.'.format(day))
        print()

    print('-'*40)
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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]


    if day != 'All':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # display the most common month
    most_frequent_month = df['month'].mode()[0]
    print('The month with the most number of travels is {}.'.format(most_frequent_month))

    # display the most common day of week
    most_frequent_day = df['day_of_week'].mode()[0]
    print('The day with the most number of travel is {}.'.format(most_frequent_day))

    # display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    print('The most common start hour is {}.'.format(most_common_start_hour))
    print()
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    count_start_station = df['Start Station'].value_counts()[most_common_start_station]
    print('The most commonly used start station is \"{}\", having been used a total'
          '\n of {} times.'.format(most_common_start_station, count_start_station))

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    count_end_station = df['End Station'].value_counts()[most_common_end_station]
    print('The most commonly used end station is \"{}\", having been used a total'
          '\n of {} times.'.format(most_common_end_station, count_end_station))

    # display most frequent combination of start station and end station trip
    df['Start and End Station'] = df['Start Station'] + df['End Station']
    most_common_start_end_station = df['Start and End Station'].mode()[0]
    count_start_end_station = df['Start and End Station'].value_counts()[most_common_start_end_station]
    print('The most commonly used combination of start and end stations are "{}'
          '\n'.format(most_common_start_end_station))
    print('This trip was taken a total of {} times.'.format(count_start_end_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is:'
          '\nin seconds: {}'
          '\nin minutes: {}'
          '\nin hours: {}'
          .format(total_travel_time, total_travel_time/60, total_travel_time/60/60))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The average travel time is:'
          '\nin seconds: {}'
          '\nin minutes: {}'
          '\nin hours: {}'
          .format(mean_travel_time, mean_travel_time/60, mean_travel_time/60/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_type = df['User Type'].value_counts()
    print('Here is the number of different user types: \n'
          '{}'.format(count_user_type))

    try:
        count_gender = df['Gender'].value_counts()
        earliest_birthyear = df['Birth Year'].min()
        most_recent_birthyear = df['Birth Year'].max()
        most_common_birthyear = df['Birth Year'].mode()[0]

    except KeyError:
        print('NO DATA -- The selected city has no Gender column')
        print('NO DATA -- The selected city has no Birth Year column')

    else:
        print('Here is the count of users by gender group:\n'
              '{}'.format(count_gender))
        print('The earliest birthyear is: {}'.format(int(earliest_birthyear)))
        print('The most recent birthyear is: {}'.format(int(most_recent_birthyear)))
        print('The most common birthyear is: {}'.format(int(most_common_birthyear)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """ Accesses csv and displays 5 rows of its raw data if user types "yes"
    (This section was copied from: https://pastebin.com/gNV8vyMc)
    I tried doing this on my own but was unable to"""


    raw_data_request = input('\nWould you like to see 5 rows of raw data?  (Yes or No)\n> ').lower()
    if raw_data_request == 'yes':
        print('\nAccessing Raw Data...\n')
        start_time = time.time()
        # index number = 0
        i = 0
        # this while loop cycles through raw data in csv and displays it
        while True:
            print(df.iloc[i:i + 5])
            i += 5
            print("\nThis took %s seconds." % (time.time() - start_time))
            more_data_request = input('\nWould you like to see 5 more rows of raw data?  (Yes or No)\n> ').lower()
            # breaks out of loop if user doesn't type "yes"
            if more_data_request != 'yes':
                break


    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        """ Asks user to restart program and clears screen if yes
        (This section was copied from: https://pastebin.com/gNV8vyMc)
        I tried doing this on my own but was unable to"""

        restart = input('\nWould you like to restart?  (Yes or No)\n> ')
        if restart.lower() == 'yes':
            # detects user os
            os_type = platform.system()
            # clears screen: OSX & Linux
            if os_type in ('Darwin', 'Linux'):
                os.system('clear')
            # clears screen: Windows
            elif os_type == 'Windows':
                os.system('cls')
            # continues without clearing screen if unknown OS is detected
            else:
                continue
        elif restart.lower() != 'yes':
            break
if __name__ == "__main__":
	main()
