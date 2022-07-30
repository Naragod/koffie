import sqlite3


class Cache:
  conn = None
  cursor = None

  def __init__(self, db_name, is_debugging_on=False):
    try:
      print("Opening db connection to:", db_name)
      # this may lead to data corruption if queries are not serialized correctly - https://stackoverflow.com/a/48234567/8714371
      self.conn = sqlite3.connect(db_name, check_same_thread=False)
      self.cursor = self.conn.cursor()

      if(is_debugging_on):
        # This attaches the tracer - for debuffing purposes
        self.conn.set_trace_callback(print)
    except Exception as e:
      print("Could not connext to database:", db_name)
      raise e

  def query(self, command, parameters=()):
    try:
      self.cursor.execute(command, parameters)
      return self.cursor.fetchall()
    except Exception as e:
      print("Could not execute query:", command, "with parameters:", parameters)
      raise e

  def commit(self):
    print("Commit changes")
    self.conn.commit()

  def close(self):
    print("Closing db connection")
    self.cursor.close()
