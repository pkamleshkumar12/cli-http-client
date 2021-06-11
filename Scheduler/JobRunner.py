import pandas as pd
from datetime import datetime
from croniter import croniter
import os
import re

if __name__ == "__main__":

    try:
        df = pd.read_csv("CronConfigurations.csv")
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        SystemExit(fnf_error)
    now = datetime.now()
    print("now:", now)
    base = datetime(now.year, now.month, now.day, now.hour, now.minute)
    print("-----Before processing-----")

    for ind in df.index:
        print(df['cron_expression'][ind],
              df['next_schedule'][ind],
              df['is_next_schedule'][ind],
              df['command'][ind],
              df['rerun'][ind]
              )

        if df['is_next_schedule'][ind] == 0:
            cron_iter = croniter(df['cron_expression'][ind], base)

            # print("df['cron_expression'][ind] ",df['cron_expression'][ind])
            # print("base", base)

            next_schedule = cron_iter.next(datetime)

            df.at[ind, 'next_schedule'] = str(next_schedule)

    # setting all is_next_schedule to 1
    df['is_next_schedule'] = 1

    # cron_expression,next_schedule,is_next_schedule,command,rerun
    os.chdir('../')
    for ind in df.index:
        next_schedule = df['next_schedule'][ind]
        sch_hr = re.findall("(\d{2}):", next_schedule)[0]
        sch_mn = re.findall("(\d{2}):", next_schedule)[1]
        now = datetime.now()
        prev_minute = now.minute - 1
        print("sch_hr: ", sch_hr, "sch_mn: ", sch_mn)
        print("now.hour", now.hour, "now.minute", now.minute)

        if str(now.hour) == sch_hr and str(now.minute) == sch_mn:
            print("time to execute")
            os.system(df['command'][ind])

            cron_iter = croniter(df['cron_expression'][ind], base)
            next_schedule = cron_iter.next(datetime)
            df.at[ind, 'next_schedule'] = str(next_schedule)
    # processing csv file

    print("\n")
    print("-----After processing-----")
    for ind in df.index:
        print(df['cron_expression'][ind],
              df['next_schedule'][ind],
              df['is_next_schedule'][ind],
              df['command'][ind],
              df['rerun'][ind])

    df.to_csv("Scheduler/CronConfigurations.csv", index=False)
    print('Overwritten CronConfiguration.csv!!')
