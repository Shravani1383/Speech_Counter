import time

 

class VirtualFriendTimer:

    def __init__(self, timer_duration):

        """

        Initialize the timer with the given duration in minutes.

       

        Args:

        timer_duration (int): Initial duration of the timer in minutes.

        """

        if not isinstance(timer_duration, int) or timer_duration <= 0:

            raise ValueError("Timer duration must be a positive integer.")

        self.timer_duration = timer_duration * 60  # Convert to seconds for internal use

        self.remaining_time = self.timer_duration

 

    def update_timer(self, message_duration):

        """

        Update the timer by subtracting the duration of an incoming voice message.

       

        Args:

        message_duration (float): Duration of the incoming message in minutes.

        """

        if not isinstance(message_duration, (int, float)) or message_duration <= 0:

            raise ValueError("Message duration must be a positive number.")

       

        # Convert message duration to seconds

        message_duration_seconds = message_duration * 60

        self.remaining_time -= message_duration_seconds

       

        # Ensure the timer doesn't go below zero

        if self.remaining_time < 0:

            self.remaining_time = 0

   

    def get_remaining_time(self):

        """

        Get the remaining time in minutes and seconds.

       

        Returns:

        (int, int): Remaining minutes and seconds.

       """

        minutes = self.remaining_time // 60

        seconds = self.remaining_time % 60

        return int(minutes), int(seconds)

   

    def display_remaining_time(self):

        """

        Display the remaining time in a human-readable format.

        """

        minutes, seconds = self.get_remaining_time()

        print(f"Remaining time: {minutes} minutes, {seconds} seconds")

 

def main():

    # Initialize the timer with a preset duration

    timer_duration = 10  # 10 minutes

    virtual_friend_timer = VirtualFriendTimer(timer_duration)

   

    # Simulate incoming voice messages with different durations

    message_durations = [2.5, 3.0, 1.25, 0.75]  # Durations in minutes

   

    # Update the timer for each incoming message

    for message_duration in message_durations:

        print(f"Processing message of duration {message_duration} minutes...")

        virtual_friend_timer.update_timer(message_duration)

        virtual_friend_timer.display_remaining_time()

        time.sleep(1)  # Simulate time delay between messages

   

    # Final remaining time

    print("Final remaining time:")

    virtual_friend_timer.display_remaining_time()

 

if __name__ == "__main__":

    main()

 