(***
 *
 * comments
 **)

PROGRAM a1 (input,output);
    USES dayio;

    CONST 
        { Open positions in the schedule. }
        NotScheduled = '        ';

        { Max length of an employee name. }
        EmployeeMaxLen = 8;

        { Hours in a day. }
        FirstHour = 8;
        LastHour = 17;          { 5:00 PM in 24-hour time }
        PastLastHour = 18;      { One past, for while loops. }

        { How much room to allow for each day in the table. }
        TableDayWidth = 9;
    TYPE 
        { The employee name type. }
        EmployeeType = string[EmployeeMaxLen];

        { The type of the schedule ARRAY. }
        { HourType = FirstHour..LastHour; }
        HourType = 8..17;
        ScheduleType = ARRAY [HourType, DayType] OF EmployeeType;
        { HourScanType = FirstHour..PastLastHour; }
        HourScanType = 8..18;

    (***********************************************************************
     * Procedure to read the next non-blank.  It skips leading blanks, then
     * reads the string up to the first blank or eoln.
     ***********************************************************************)
    PROCEDURE ReadString(VAR Str: string);
        VAR
            Ch: char;
        BEGIN
            Ch := ' ';
            WHILE (Ch = ' ') AND NOT eoln DO 
                read(Ch);

            IF Ch = ' ' THEN
                { There is no command on this line. }
                Str := ''
            ELSE
                BEGIN 
                    { Read the beast. }
                    Str := '';
                    WHILE (Ch <> ' ') AND NOT eoln DO
                        BEGIN
                            Str := Str + Ch;
                            read(Ch)
                        END;

                    IF Ch <> ' ' THEN
                        { Command ended at eoln. }
                        Str := Str + Ch
                END
        END; { ReadString }

    (***********************************************************************
     * Procedure to read the arguments held in common by the sched 
     ***********************************************************************)
    PROCEDURE ReadSchedClrArgs(
            VAR StartDay, EndDay: DayType;      { Input days. }
            VAR StartHour, EndHour: HourType;   { Input hour range. }
            VAR Error: boolean);                { Input error indicator.}
        VAR
            InputHour: integer;                 { Input hour value. }

        { Map time to 24-hours based on the AM/PM rules. }
        FUNCTION MapTo24(Hour: integer): HourType;
            CONST
                { AM/PM time cut-off. }
                LastPM = 5;
            BEGIN
                IF Hour <= LastPM THEN
                    MapTo24 := Hour + 12
                ELSE
                    MapTo24 := Hour
            END;

        BEGIN { ReadSchedClrArgs }
            { Read the days. }
            ReadDay(input, StartDay);
            ReadDay(input, EndDay);

            { See if they both worked. }
            IF (StartDay <> BadDay) AND (EndDay <> BadDay) THEN 
                BEGIN
                    { It worked.  Read the hours. }
                    read(InputHour);
                    StartHour := MapTo24(InputHour);
                    read(InputHour);
                    EndHour := MapTo24(InputHour);

                    { Report success }
                    Error := FALSE 
                END
            ELSE
                (* Something went wrong, seriously wrong. *)
                Error := TRUE;

            (* We're done with this line. *)
            readln
        END; { ReadSchedClrArgs }

    {****************************************************************
     * PROCEDURE to print headers of each day.
     *  Precondition: None.
     *  Postcondition: A header line with the days of the week has
     *    been printed.  The 
     ****************************************************************}
    PROCEDURE WriteDaysHeader;
        CONST

            { How many spaces to move over before printing days-of
              the week header. }
            DaysHeadMoveOver = 6;

            { How much room to assume is needed by each day string. }
            AllowForDay = 3;
        VAR
            Day: DayType;
        BEGIN
            write(' ': DaysHeadMoveOver);

            FOR Day := Sun TO Sat DO
                BEGIN
                    write('[ ');
                    WriteDay(output, Day);
                    write(' ]', ' ': TableDayWidth - AllowForDay - 4)
                END;
            writeln
        END; { WriteDaysHeader }

    {****************************************************************
     * Function that tells if a pending schedule is legal.
     ****************************************************************}
    FUNCTION SchedLegal(
            VAR Schedule: ScheduleType;     { Schedule to check. }
                StartDay, EndDay: DayType;  { Days in question. }
                FirstHour, LastHour:        { Hours in question. }
                        HourType): boolean;
        VAR
            ConflictFound: boolean;         { Tell if one found. }
            DayScan: DayType;               { Go through the days. }
            HourScan: HourScanType;         { Go through the hours. }
        BEGIN
            { Scan the days. }
            DayScan := StartDay;
            ConflictFound := FALSE;
            REPEAT
                { For this day, scan the times. }
                HourScan := FirstHour;
                WHILE NOT ConflictFound AND
                                (HourScan <= LastHour) DO BEGIN
                    { Conflict? }
                    ConflictFound :=
                            Schedule[HourScan, DayScan] <> NotScheduled;

                    { Next one. }
                    HourScan := HourScan + 1
                END;

                { Next Day. }
                DayScan := succ(DayScan)
            UNTIL ConflictFound or (DayScan > EndDay);

            { And the answer is.. }
            SchedLegal := not ConflictFound
        END; { SchedLegal }

    {****************************************************************
     * This takes care of most of the work of the clear and sched
     ****************************************************************}
    PROCEDURE SetSchedPart(
            VAR Schedule: ScheduleType;     { Set me! Set me! }
                Employee: EmployeeType;     { Who gets to work. }
                StartDay, EndDay: DayType;  { Days in question. }
                FirstHour, LastHour:        { Hours in question. }
                                HourType);
        VAR
            DayScan: DayType;               { Go through the days. }
            HourScan: HourType;             { Go through the hours. }
        BEGIN
            for DayScan := StartDay to EndDay do
                for HourScan := FirstHour to LastHour do
                    Schedule[HourScan, DayScan] := Employee
        END; { SetSchedPart }

    {****************************************************************
     * Perform the sched command.
     *  Precondition: The read pointer is followed by the arguments 
     ****************************************************************}
    PROCEDURE DoSched(
            VAR Schedule: ScheduleType);    { Change this. }
        VAR
            Employee: EmployeeType;         { Input employee name. }
            StartDay, EndDay: DayType;      { Input days. }
            StartHour, EndHour: HourType;   { Input hour range. }
            Error: boolean;                 { Input error indicator.}
        BEGIN
            { Read the employee name }
            ReadString(Employee);

            { Read all the other arguments, and recieve error 
               indication. }
            ReadSchedClrArgs(StartDay, EndDay, StartHour, EndHour, Error);

            { For errors, let 'em know.  Otherwise, do it. }
            IF Error THEN
                writeln('*** Un-recognized day code.  ',
                    'Command not performed. ***')
            ELSE 
                { See if the scheduling is legal. }
                IF SchedLegal(Schedule, StartDay, EndDay,
                                        StartHour, EndHour) THEN
                    BEGIN
                        { Legal.  Do it and admit it. }
                        SetSchedPart(Schedule, Employee,
                                StartDay, EndDay, StartHour, EndHour);
                        writeln('>>> ', Employee, ' scheduled. <<<')
                    END
                ELSE 
                    { Not legal. }
                    writeln('*** Conflicts with existing schedule.  ',
                        'Command not performed. ***')
        END; { DoSched }

    {****************************************************************
     * Perform the clear command.
     ****************************************************************}
    PROCEDURE DoClear(
            VAR Schedule: ScheduleType);    { Change this. }
        VAR
            StartDay, EndDay: DayType;      { Input days. }
            StartHour, EndHour: HourType;   { Input hour range. }
            Error: boolean;                 { Input error indicator.}
        BEGIN
            { Read the arguments, and recieve error indication. }
            ReadSchedClrArgs(StartDay, EndDay, StartHour, EndHour, Error);

            { For errors, let 'em know.  Otherwise, do it. }
            IF Error THEN
                writeln('*** Un-recognized day code.  ',
                    'Command not performed. ***')
            ELSE 
                BEGIN
                    SetSchedPart(Schedule, NotScheduled, StartDay, EndDay,
                        StartHour, EndHour);
                    writeln('>>> Clear performed. <<<');
                END { DoClear }
        END;

    {****************************************************************
     * Peform the unsched command.
     ****************************************************************}
    PROCEDURE DoUnsched(
            VAR Schedule: ScheduleType);        { Remove from. }
        VAR
            Employee: EmployeeType;             { To remove. }
            Day: DayType;                       { Column scanner. }
            Hour: integer;                      { Row scanner. }
            Found: boolean;                     { Presence indicator }
        BEGIN
            { Read the employee. }
            readln(Employee);

            { Remove! Remove! }
            Found := FALSE;
            FOR Day := Sun TO Sat DO
                FOR Hour := FirstHour TO LastHour DO
                    IF Schedule[Hour, Day] = Employee THEN 
                        BEGIN
                            { Remove. }
                            Schedule[Hour, Day] := NotScheduled;

                            { Note. }
                            Found := TRUE 
                        END;

            { Warn if not found. Else just state. }
            IF Found THEN 
                write('>>> ', Employee, ' removed from schedule. <<<')
            ELSE
                write('>>> ', Employee, 
                                    ' was not on the schedule. <<<')
        END; { DoUnsched }

    PROCEDURE DoPrint(
            VAR Schedule: ScheduleType);        { Print me. }
        VAR
            Hour: HourType;                     { Hour scan. }
            Day: DayType;                       { Day scan. }

        { Map }
        FUNCTION Map24to12(HourType: HourType): integer;
            BEGIN
                IF Hour < 13 THEN
                    Map24to12 := Hour
                ELSE
                    Map24to12 := Hour - 12
            END;
        BEGIN
            readln;
            WriteDaysHeader;

            FOR Hour := FirstHour TO LastHour DO
                BEGIN
                    write(Map24to12(Hour):2, ':00 ');
                    FOR Day := Sun TO Sat DO
                        write(Schedule[Hour, Day], 
                            ' ': TableDayWidth - length(Schedule[Hour, Day]));
                    writeln
                END
        END;

    PROCEDURE DoTotal(
            VAR Schedule: ScheduleType);        { The schedule. }
        VAR
            Employee: EmployeeType;             { To remove. }
            Day: DayType;                       { Column scanner. }
            Hour: integer;                      { Row scanner. }
            Total: integer;                     { Total intgers. }
        BEGIN
            { Read the employee. }
            readln(Employee);

            { Do the sum. }
            Total := 0;
            FOR Day := Sun TO Sat DO
                FOR Hour := FirstHour TO LastHour DO
                    IF Schedule[Hour, Day] = Employee THEN
                        Total := Total + 1;

            { Write the total. }
            writeln('>>> ', Employee,
                ' is scheduled for ', Total:1, ' hours. <<<<')
        END; { DoTotal }

    {*****************************************************************
     * Main line.
     *****************************************************************}

    VAR
        { The schedule. }
        Schedule: ScheduleType;

        { Main loop continue flag. }
        KeepRunning: boolean;

        { Command input local to main. }
        Command: string;

    BEGIN
        { Clear the schedule. }
        SetSchedPart(Schedule, NotScheduled, Sun, Sat, FirstHour, LastHour);
 
        { Do the commands. }
        write('==> ');
        ReadString(Command);
        KeepRunning := TRUE;
        WHILE KeepRunning DO
            BEGIN
                IF Command = 'sched' THEN 
                    DoSched(Schedule)
                ELSE IF Command = 'clear' THEN
                    DoClear(Schedule)
                ELSE IF Command = 'unsched' THEN
                    DoUnsched(Schedule)
                ELSE IF Command = 'print' THEN
                    DoPrint(Schedule)
                ELSE IF Command = 'total' THEN
                    DoTotal(Schedule)
                ELSE IF Command = 'quit' THEN 
                    BEGIN
                        writeln;
                        writeln('>>> Program terminating. <<<');
                        KeepRunning := FALSE
                    END
                ELSE
                    { Command not recognized. }
                    BEGIN
                        readln;
                        writeln;
                        writeln('*** Command ', Command, 
                                                    ' not recognized. ***');
                    END;

                { Go to a new page for next'n. }
                write('==> ');
                ReadString(Command)
            END
    END.