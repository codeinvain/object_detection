from networktables import NetworkTables 
import threading as th
import signal
import tracks


class TableManager:
    def __init__(self, detection_status_method):
        self.do_work_lock = th.Lock()
        self.set_detection_status = detection_status_method
        self.do_work = False

        self.load_config()

        self.init_signals()
        if (tracks.config['networktables']==True):
            tracks.logger.debug('started communications module with networktable')
            self.init_network_tables()
        else:
            tracks.logger.debug('started communications module without networktable')


    def load_config(self):
        """Load data from config file"""
        self.do_work_name = tracks.config['table_names']['do_work']
        self.horizontal_data_name = tracks.config['table_names']['horizontal_data_name']
        self.vertical_data_name = tracks.config['table_names']['vertiacl_data']
        self.angle_data_name = tracks.config['table_names']['angle_data_name']


    def init_signals(self):
        """signals support when no networktables available"""
        signal.signal(signal.SIGUSR1, self.mock_network_tables)
        signal.signal(signal.SIGUSR2, self.mock_network_tables)

    def init_network_tables(self):
        """Connection and setup of the networktables"""
        NetworkTables.initialize(server=tracks.config['server'])
        self.vision_table = NetworkTables.getTable(tracks.config['table_names']['main_table'])
        self.do_work = self.vision_table.getBoolean(self.do_work_name, False)

        self.vision_table.putString(self.horizontal_data_name, 'L0')
        self.vision_table.putString(self.angle_data_name, 'L0')
        self.vision_table.putNumber(self.vertical_data_name, 0)
        self.vision_table.putBoolean(self.do_work_name, False)

        self.vision_table.addTableListener(self.do_work_changed, True, self.do_work_name, False)

        tracks.logger.debug('connected to networktable')


    def mock_network_tables(self,signum, stack):
        if (signum==signal.SIGUSR1):
            self.set_do_work(True)
            self.set_detection_status(self.get_do_work())
            
        if (signum==signal.SIGUSR2):
            self.set_do_work(False)
            self.set_detection_status(self.get_do_work())

        

    def publish_target_data(self, horizontal_distance, horizontal_vector, angle_to_target, vertical_distance):
        """
        Publish navigation data to target

        Publish the data needed to navigate to the target

        Parameters
        ----------
        horizontal_distance : int
            The horizontal distance to the target
        horizontal_vector : string
            The side to the target. L for left, R for right
        vertical_distance : int
            The vertical distance to the target

        Returns
        -------
        void
        """
        if (tracks.config['networktables']==True):
            self.vision_table.putString(self.horizontal_data_name, horizontal_vector + str(horizontal_distance))
            self.vision_table.putString(self.angle_data_name, horizontal_vector + str(angle_to_target))
            self.vision_table.putNumber(self.vertical_data_name, vertical_distance)
        else:
            tracks.logger.debug("would send coordinate distance_x:{0}{1} distance_y:{2} angle:{3} ".format(horizontal_vector,horizontal_distance,vertical_distance,angle_to_target))

    def get_do_work(self):
        """Return the value of do_work (thread-safe)"""
        with self.do_work_lock:
            return self.do_work

    def set_do_work(self, value):
        """Set the value of do_work (thread-safe)"""
        with self.do_work_lock:
            if type(value) is type(self.do_work):
                self.do_work = value

    def is_do_work(self):
        """Return True if the robot requesting calculation for target navigation"""
        return self.get_do_work()

    def start_work(self):
        """Start the work loop"""
        self.set_detection_status(self.get_do_work())
        # th.Thread(target=self.work_loop).start()

    # def work_loop(self):
        # """Start work given while do_work is True"""
        # is_do_work = self.get_do_work()

        # while is_do_work:
            # self.work()
            # is_do_work = self.get_do_work()

    def do_work_changed(self, table, key, value, isNew):
        """
        Handle change in the work request indicator

        While the indecator is True the work method is called, if False stop doing work
        """
        if key == self.do_work_name:
            tracks.logger.debug('do work changed to ' + str(value))
            self.set_do_work(value)
            if value is True:
                self.start_work()
