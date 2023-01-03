import time
import pandas as pd
import numpy as np

pd.set_option('max_columns', None)

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

month_dict = { '1' : 'January',
               '2' : 'February',
               '3' : 'March',
               '4' : 'April',
               '5' : 'May',
               '6' : 'June' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nWhich city would you like to explore today - Chicago, New York city, or Washington ? : \n").lower()
        if city in ['chicago', 'new york city', 'washington']:
            print("Okay ... {} it is !".format(city.title()))
            break
        print("Wrong input ! Please input a city amongst these 3 cities : \n Chicago \n New York City \n Washington")

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nWhich month ? \nJanuary, February, March, April, May, or June?. For all months, please enter 'all' : \n").lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            print("Okay ... In {}, we are looking at {} month(s). ".format(city.title(), month.title()))
            break
        print("Wrong input ! Please input a month amongst the 6 mentioned ones, or 'all'.\n")


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nWhich day ? \nMonday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? \nFor all days, please enter 'all' : \n").lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            if day != 'all':
                print("Okay ... In {}, we are looking at {} month(s) and {}s ".format(city.title(), month.title(), day.title()))
            else:
                print("Okay ... In {}, we are looking at {} month(s) and {} days ".format(city.title(), month.title(), day.title()))
            break
        print("Wrong input ! Please input a valid day name, or 'all'.")


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if df['month'].value_counts().shape[0] > 1:
        popular_month = df['month'].mode()[0]
        popular_month_name = month_dict[str(popular_month)]
        print("\nMost common month amongst all months in the data : {}".format(popular_month_name))
    else:
        month_name = month_dict[str(df['month'].value_counts().index[0])]
        print("\nFor the selected month {}".format(month_name))

    # TO DO: display the most common day of week
    if df['day_of_week'].value_counts().shape[0] > 1:
        popular_day = df['day_of_week'].mode()[0]
        print("\nMost common day amongst all days is {}".format(popular_day))
    else:
        print("\nFor the selected day {}".format(df['day_of_week'].value_counts().index[0]))


    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print("\nMost common start hour is {}".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('\nMost common start station for your selection is {}'.format(popular_start_station.title()))

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('\nMost common end station for your selection is {}'.format(popular_end_station.title()))


    # TO DO: display most frequent combination of start station and end station trip
    #df1 = df['Start Station', 'End Station'].value_counts()
    df['Route'] = df['Start Station'] + " -- " + df['End Station']
    popular_route = df['Route'].mode()[0]
    print('\nMost common route for your selection "Start Station -- End Station" is {}'.format(popular_route.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['Trip Duration'] = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])
    total_trip_duration = df['Trip Duration'].dt.total_seconds().sum()
    print("Total trip duration for your selection is {} seconds".format(total_trip_duration))

    # TO DO: display mean travel time
    avg_trip_duration = df['Trip Duration'].dt.total_seconds().mean()
    print("Average trip duration for your selection is {} seconds".format(avg_trip_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("\nDifferent types of users with their count : \n")
    print(df['User Type'].value_counts())

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        df['Gender'].fillna(value = 'Not Specified', inplace = True)
        print("\nDifferent types of genders with their count : \n")
        print(df['Gender'].value_counts())

    # TO DO: Display earliest, most recent, and most common year of birth

    if 'Birth Year' in df.columns:
        earliest_yob = df['Birth Year'].min()
        latest_yob = df['Birth Year'].max()
        common_yob = df['Birth Year'].mode()[0]

        print("\nThe earliest birth year is {} \nThe latest birth year is {} \nThe most common birth year is {}".format(earliest_yob, latest_yob, common_yob))
        print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def individual_trips(df):
    counter = 0
    ans = input('\nWould you like to view data for individual trips ? Enter yes or no.\n')
    if ans.lower() == 'yes':
        while True:
            print(df[counter:counter+5])
            counter += 5
            ans = input('\nWould you like to view more? Enter yes or no.\n')
            if ans.lower() != 'yes':
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        #print(city, month, day)
        #print(df.isnull().any())

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        individual_trips(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
