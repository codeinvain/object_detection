from networktables import NetworkTables 
import threading as th
import signal
import tracks


TABLE_NAME = 'ImageProc'
DO_WORK_NAME = 'calculate'
HORIZONTAL_DATA_NAME = 'horizontal'
VERTICAL_DATA_NAME = 'vertical'

class TableManager:
    def __init__(self, detection_status_method):
        self.do_work_lock = th.Lock()
        self.set_detection_status = detection_status_method
        self.do_work = False

        self.init_signals()
        if (tracks.config['networktables']==True):
            self.init_network_tables()


    def init_signals(self):
        """signals support when no networktables available"""
        signal.signal(signal.SIGUSR1, self.mock_network_tables)
        signal.signal(signal.SIGUSR2, self.mock_network_tables)

    def init_network_tables(self):
        """Connection and setup of the networktables"""
        NetworkTables.initialize(server='10.43.20.2')
        self.vision_table = NetworkTables.getTable(TABLE_NAME)
        self.do_work = self.vision_table.getBoolean(DO_WORK_NAME, False)

        self.vision_table.addTableListener(self.do_work_changed, True, DO_WORK_NAME, False)


    def mock_network_tables(self,signum, stack):
        if (signum==signal.SIGUSR1):
            self.set_do_work(True)
            self.set_detection_status(self.get_do_work())
            
        if (signum==signal.SIGUSR2):
            self.set_do_work(False)
            self.set_detection_status(self.get_do_work())

        

    def publish_target_data(self, horizontal_distance, horizontal_vector, vertical_distance):
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
            self.vision_table.putString(HORIZONTAL_DATA_NAME, horizontal_vector + str(horizontal_distance))
            self.vision_table.putNumber(VERTICAL_DATA_NAME, vertical_distance)
        else:
            tracks.logger.debug("would send coordinate distance_x:{0} distance_y:{1} angle:{2} ".format(horizontal_distance,horizontal_vector,vertical_distance))

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
        if key == DO_WORK_NAME:
            self.set_do_work(value)
            if value is True:
                self.start_work()
