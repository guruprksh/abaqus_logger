import os
import time
import inspect


class SimpleLogger(object):

    def __init__(
        self,
        model_name,
        work_dir,
        log_name=None,
        overwrite=True
    ):

        self.model_name = model_name
        self.work_dir = work_dir
        self.start_time = time.time()
        self.rows = []

        if log_name:
            cae_name = log_name
        else:
            cae_name = self._get_log_name()

        self.log_file = os.path.join(
            self.work_dir,
            "{}_log.txt".format(cae_name)
        )
        if overwrite:
            try:
                if os.path.isfile(self.log_file):
                    os.remove(self.log_file)
            except Exception:
                pass

    def _get_log_name(self):
        """
        Determine log file name.

        Priority:
        1. Abaqus CAE file name
        2. Calling script name
        3. unsaved_model
        """

        try:
            if mdb.pathName:
                return os.path.splitext(
                    os.path.basename(mdb.pathName)
                )[0]
        except Exception:
            pass

        try:

            current_file = os.path.abspath(__file__)

            for frame in inspect.stack():

                filename = os.path.abspath(frame[1])

                if filename != current_file:

                    return os.path.splitext(
                        os.path.basename(filename)
                    )[0]

        except Exception:
            pass

        return "unsaved_model"

    def add_header(
        self,
        title,
        char="=",
        pad=2
    ):
        self.rows.append(
            ["__HEADER__", title, char, pad]
        )

    def add_separator(
        self,
        char="-",
        length=None
    ):
        self.rows.append(
            ["__SEPARATOR__", char, length]
        )

    def add(
        self,
        step,
        status,
        message
    ):

        elapsed = round(
            time.time() - self.start_time,
            2
        )

        self.rows.append(
            [
                str(step),
                str(status),
                str(message),
                str(elapsed)
            ]
        )

    def save(self):

        col_count = 4
        col_widths = [0] * col_count

        for row in self.rows:

            if row[0] in (
                "__HEADER__",
                "__SEPARATOR__"
            ):
                continue

            for i in range(col_count):

                col_widths[i] = max(
                    int(col_widths[i]),
                    len(str(row[i]))
                )

        # Full table width: column widths plus " | " separators
        total_width = sum(col_widths) + 3 * (col_count - 1)

        if total_width < 50:
            total_width = 50

        # The output folder may have been purged after the logger was created
        if self.work_dir and not os.path.isdir(self.work_dir):
            os.makedirs(self.work_dir)

        with open(self.log_file, "w") as f:

            for row in self.rows:

                if row[0] == "__SEPARATOR__":

                    sep_char = str(row[1])[0]

                    if row[2] is not None:
                        length = int(row[2])
                    else:
                        length = int(total_width)

                    f.write(
                        sep_char * length + "\n"
                    )

                elif row[0] == "__HEADER__":

                    title = (
                        " " * int(row[3])
                        + str(row[1])
                        + " " * int(row[3])
                    )

                    fill = int(
                        max(
                            int(total_width) - len(title),
                            0
                        )
                    )

                    left_fill = int(fill // 2)
                    right_fill = int(fill - left_fill)

                    header = (
                        str(row[2])[0] * left_fill
                        + title
                        + str(row[2])[0] * right_fill
                    )

                    f.write(header + "\n")

                else:

                    line = " | ".join(
                        str(row[i]).ljust(
                            int(col_widths[i])
                        )
                        for i in range(col_count)
                    )

                    f.write(line + "\n")

        print(
            "Log saved to: {}".format(
                self.log_file
            )
        )
