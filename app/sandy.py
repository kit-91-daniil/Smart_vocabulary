"""Устанавливает время в секундах до следующего опроса.
        Порядок действий:
        <st> time_diff = iw_inst.repeating_time - datetime.now() --> timedelta(days=int, seconds=int)
        <st> total_seconds = timediff.total_seconds() - Количtство секунд. Заносится в базу данных
            = time_to_repeat
        <st> В зависимости от знака и количества секунд разделение на группы:
            1) Отрицательное количество секунд:
                1.1 По модулю больше 86400 - цикл повторения будет начат заново
                filter(IntervalWords.time_to_repeat <= 86400 )
                    -- lost_test_days, lost_test_time = str(timedelta(seconds=total_seconds)).split(" days, ")
                    -- lost_test_hours, lost_test_minutes = lost_test_time.split(":")[1:]
                1.2 По модулю менее 86400 - Пропущенные тесты
                filter(IntervalWords.time_to_repeat <= 0,
                IntervalWords.time_to_repeat >= -86400)
                    -- missing_test_hours, missing_test_minutes = str(timedelta(seconds=total_seconds)).split(":")[1:]

            2) Положительное количество секунд:
                 2.1 кол-во секунд < 7200 но больше 0, текущий тест
                filter(IntervalWords.time_to_repeat > 0,
                IntervalWords.time_to_repeat < 7200)
                    -- near_test_days, near_test_time = str(timedelta(seconds=total_seconds)).split(" days, ")
                    -- near_test_hours, near_test_minutes = near_test_time.split(":")[1:]

        <st> days_time_tpl = str(timedelta(seconds=total_seconds)).split(" days, ")
            Время в часах, минутах, секундах
        <st> days_quantity = int(total_sec_str.split("days")[0]) ("23455")
        <st> time_ = total_sec_str.split("days")[1] ("12:12:12")
        <st> hours, minutes = time_.split(":")[1:]

        """