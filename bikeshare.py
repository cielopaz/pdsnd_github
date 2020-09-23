#github mandated step
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_LIST = ['January', 'February', 'March', 'April', 'May', 'June', 'all']

DAY_LIST = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'all']


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
    city = input ('Which city would you like to analyze? chicago, new york, washington?').lower()
    while city not in CITY_DATA:
        print('Sorry we were not able to get data for that city.  Please select chicago, new york city or washington instead.')
        city = input('Which city would you like to analyze? chicago, new york, or washington?')

    print('You selected: ', city)

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Which month would you like to look at? Select January to June only or all six months.')
    while month not in MONTH_LIST:
        print('The month you selected is not available. Please select from January to June only.')
        month = input('Which month would you like to look at? Select January to June only or all six months.')

    print('You selected: ', month)
        
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    day = input('Which day would you like to look at?  Or do you want to see all days?')
    while day not in DAY_LIST:
        print('There was an error in your selection.')
        day = input('Which day would you like to look at?  Or do you want to see all days?')

    print('You selected: ', day)

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

    df = pd.read_csv(CITY_DATA[city],low_memory=False)
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['End Time']=pd.to_datetime(df['End Time'])    
    print(df.dtypes)
    print(df.isna().describe())
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    df['city'] = city
    print(df['day_of_week'])
    
    #filter by month if applicable
    print(month)
    if month !='all':
         #use the index of the months list to get the corresponding int
            months = ['January', 'February', 'March', 'April', 'May', 'June']
            month = MONTH_LIST.index(month) + 1
            
             #filter by month to create the new dataframe
            df = df[df['month'] == month]
    
     # filter by day of week if applicable
    print(day)
    if day !='all':
         #filter by day of week to create the new dataframe
            df = df[df['day_of_week'] == day]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month_number = df['month'].mode()[0]
    common_month = MONTH_LIST[common_month_number-1].title()
    print("The most popular month in', city, 'is", common_month)
    print("Oops! something went wrong.  Please make selection again.")
    
    # TO DO: display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print("The most popular weekday in', city, 'is", common_day_of_week)

    # TO DO: display the most common start hour
    common_start_hour = df['hour'].mode()[0]
    print("The most popular starting hour in', city, 'is", common_start_hour)
                                

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    city_val = df['city'].unique()[0]
    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    common_start_station_number = df['Start Station'].value_counts()[0]
    print('The most commonly used start station in', city_val, 'is:',common_start_station, 'which was used', common_start_station_number, 'times.')

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    popular_end_station_amount = df['End Station'].value_counts()[0]
    print('The most popular end station in', city_val, 'is:',popular_end_station, 'and was used', popular_end_station_amount, 'times.')
    
    # TO DO: display most frequent combination of start station and end station trip
    frequent_trip = df.loc[:, 'Start Station':'End Station'].mode()[0:]
    frequent_trip_amt = df.groupby(["Start Station", "End Station"]).size().max()
    print('the most frequent trip is:\n', frequent_trip, '\n and was made', frequent_trip_amt,'times')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['Travel Time'] = df['End Time'] - df['Start Time']
    total_travel_time = df['Travel Time'].sum()
    print('The total travel time was:', total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Travel Time'].mean()
    print('The mean travel time was:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The user type count in' + df['city'].unique()[0] + 'are:' + '\n' + str(user_types))
    
    # TO DO: Display counts of gender
    gender = df['Gender'].value_counts()
    
    print('The amount of users by gender in' + df['city'].unique()[0] + 'are:' + '\n' + str(gender))


    # TO DO: Display earliest, most recent, and most common year of birth
    earliest_year = df['Birth Year'].min()
    most_recent_year = df['Birth Year'].max()
    most_common_year = df['Birth Year'].mode()
    print('The oldest user in' + df['city'].unique()[0] + 'was born in:' + str(int(earliest_year)),'\n'+'The youngest user was born in:'+ str(int(most_recent_year)) + '\n' + 'However, most users are born in:' + str(int(most_common_year)))      
                
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
# request user if they want to see lines of raw data
    # TO DO: get user input for 5 lines of raw data HINT: Use a while loop to handle invalid inputs
    looping ='yes'
    while(looping=='yes'):
        user = input('Do you want to see 5 lines of raw data? Enter yes or no')
        if user == 'no':
            print('thanks for participating')
            break
        if user == 'yes':
            print(df.iloc[0:5])
            break
    
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()