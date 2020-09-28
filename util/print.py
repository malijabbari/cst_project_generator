from datetime import datetime


class Print:
    print_log = True

    def __init__(self, path_log, job_id):
        self.path_log = path_log

        # create empty file
        print(self.path_log)
        with open(self.path_log, 'w') as file:
            file.write('')

        # write job-id
        self.log('job_id = %i' % job_id)

    @staticmethod
    def _timestamp():
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + ' |   '

    @staticmethod
    def _indent():
        return ' ' * 23 + ' |   '

    def log(self, msg):
        # print log to console
        if self.print_log:
            print(msg)

        # append message to log
        with open(self.path_log, 'a') as file:

            # split msg at linebreaks
            for idx, line in enumerate(msg.splitlines()):

                # write either a timestamp or indent
                if idx is 0:
                    file.write(self._timestamp())
                else:
                    file.write(self._indent())

                # write the line
                file.write(line + '\n')
