from networktables import NetworkTables 
import threading as th

TABLE_NAME = 'ImageProc'
DO_WORK_NAME = 'calculate'
HORIZONTAL_DATA_NAME = 'horizontal'
VERTICAL_DATA_NAME = 'vertical'
ANGLE_DATA_NAME = 'angle'

class TableManager:
    def __init__(self, work_method):
        self.startup()

        self.vision_table = NetworkTables.getTable(TABLE_NAME)
        self.do_work = self.vision_table.getBoolean(DO_WORK_NAME, False)
        self.work = work_method
        self.do_work_lock = th.Lock()

        self.vision_table.putString(HORIZONTAL_DATA_NAME, 'L0')
        self.vision_table.putString(ANGLE_DATA_NAME, 'L0')
        self.vision_table.putNumber(VERTICAL_DATA_NAME, 0)
        self.vision_table.putBoolean(DO_WORK_NAME, False)

        self.vision_table.addTableListener(self.do_work_changed, True, DO_WORK_NAME, False)

    def startup(self):
        """Connection and setup of the networktables"""
        NetworkTables.initialize(server='10.43.20.2')

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
        self.vision_table.putString(HORIZONTAL_DATA_NAME, horizontal_vector + str(horizontal_distance))
        self.vision_table.putString(ANGLE_DATA_NAME, horizontal_vector + str(angle_to_target))
        self.vision_table.putNumber(VERTICAL_DATA_NAME, vertical_distance)

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
        th.Thread(target=self.work_loop).start()

    def work_loop(self):
        """Start work given while do_work is True"""
        is_do_work = self.get_do_work()

        while is_do_work:
            self.work()
            is_do_work = self.get_do_work()

    def do_work_changed(self, table, key, value, isNew):
        """
        Handle change in the work request indicator

        While the indecator is True the work method is called, if False stop doing work
        """
        if key == DO_WORK_NAME:
            self.set_do_work(value)
            if value is True:
                self.start_work()
