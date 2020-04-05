import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    while True:
        city = (input('\nPlease enter the city you are interested in (Chicago, New York City or Washington): \n')).lower()
        if city in CITY_DATA:
            break
        else:
            print('Please enter one of these Cities: Chicago, New York City or Washington')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = (input('\nPlease enter the month you are interested in (all, January, February, ..., June): \n')).lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print('Sadly only months January to June are represented in the data. Please try again.')


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = (input('\nPlease enter the weekday name you are interested in (all, Monday, Tuesday, ..., Sunday): \n')).lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        else:
            print('Provide the weekday name in the following format: Monday, Tuesday, Wednesday, ... Please try again.')

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
        df - pandas DataFrame containing city data filtered by month and day
    """
    filename = CITY_DATA[city]

    # load data file into a dataframe
    df = pd.read_csv(filename)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

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

    # display the most common month
    popular_month_int = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month_str = months[popular_month_int-1].title()
    print('\n...Most Frequent Month of Travel: {}\n'.format(popular_month_str))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('\n...Most Frequent Day of Travel: {}\n'.format(popular_day))

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('\n...Most Common Start Hour: {}\n'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('\... Most Popular Start Station: {}\n'.format(popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('\... Most Popular End Station: {}\n'.format(popular_end_station))

    # generate a trip column
    df['trip'] = df['Start Station'].astype(str) + ' to ' + df['End Station'].astype(str)

    # display most frequent trip
    popular_trip = df['trip'].mode()[0]
    print('\... Most Popular Trip: From {}\n'.format(popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('\n...Total Travel Time: {}\n'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\n...Mean Travel Time: {:.2f}\n'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    print('\n...Count of User Types:\n{}\n'.format(user_type_counts.to_string()))

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('\n...Count of Genders:\n{}\n'.format(gender_counts.to_string()))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birthyear = df['Birth Year'].min()
        print('\n...Earliest Birth Year: {}\n'.format(int(earliest_birthyear)))

        most_recent_bithyear = df['Birth Year'].max()
        print('\n...Most Recent Birth Year: {}\n'.format(int(most_recent_bithyear)))

        most_common_birthyear = df['Birth Year'].mode()[0]
        print('\n...Most Common Birth Year: {}\n'.format(int(most_common_birthyear)))

    print('-'*40)


def display_raw(df):
    """
    display raw data that fits the previously provided filters and print the
    data in chunks of 5 lines if the user wants to see more.
    """

    start_loc = 0
    end_loc = 5

    display_active = input('\nWould you like to see raw data? Enter yes if you do.\n').lower()

    if display_active.lower() == 'yes':
        while end_loc <= df.shape[0] - 1:

            print(df.iloc[start_loc:end_loc,:])
            start_loc += 5
            end_loc += 5

            continue_display = input('\nDon\'t have enough yet? Enter yes if you don\'t.\n').lower()
            if continue_display.lower() != 'yes':
                break



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw(df)

        restart = input('\nWould you like to restart? Enter yes if you do.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
