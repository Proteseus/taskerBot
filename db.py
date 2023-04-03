import sqlite3


def connector():
    conn = sqlite3.connect('db/members.sqlite')
    cur = conn.cursor()
    return conn, cur


class Database:
    def __init__(self):
        conn, cur = connector()
        cur.execute("""CREATE TABLE IF NOT EXISTS members (
                        id INTEGER PRIMARY KEY autoincrement,
                        user TEXT NOT NULL,
                        role INTEGER NOT NULL,
                        FOREIGN KEY(role) REFERENCES roles(role_id))
                        """)
        conn.commit()
        cur.execute("""CREATE TABLE IF NOT EXISTS roles (
                        role_id INTEGER PRIMARY KEY autoincrement,
                        role TEXT NOT NULL);
                        """)
        conn.commit()
        cur.execute("""CREATE TABLE IF NOT EXISTS task_user (
                        user_id INTEGER NOT NULL,
                        task_id INTEGER NOT NULL,
                        FOREIGN KEY(user_id) REFERENCES members(id),
                        FOREIGN KEY(task_id) REFERENCES tasks(task_id));
                        """)
        conn.commit()
        cur.execute("""CREATE TABLE IF NOT EXISTS tasks (
                        task_id INTEGER PRIMARY KEY autoincrement,
                        task_desc TEXT NOT NULL,
                        due_date DATE NOT NULL);
                        """)
        conn.commit()
        cur.close()
        conn.commit()
        conn.close()

    def fetch_members(self):
        conn, cur = connector()
        cur.execute("""SELECT user, r.role
                        FROM members
                        INNER JOIN roles r on r.role_id = members.role
                        """)
        members = cur.fetchall()
        cur.close()
        conn.close()
        return members

    def fetch_member(self, name: str):
        conn, cur = connector()
        cur.execute("""SELECT user, r.role
                        FROM members
                        INNER JOIN roles r on r.role_id = members.role
                        WHERE user=?""", (name, ))
        members = cur.fetchall()
        cur.close()
        conn.close()
        return members

    def fetch_task(self):
        conn, cur = connector()
        cur.execute("""SELECT * FROM tasks""")
        tasks = cur.fetchall()
        cur.close()
        conn.close()
        return tasks

    def fetch_task_assigned(self):
        conn, cur = connector()
        cur.execute("""select
                          id,
                          user,
                          roles.role,
                          tasks.task_desc,
                          tasks.due_date
                        from
                          members
                          inner join roles ON roles.role_id = members.role
                          join task_user on task_user.user_id = members.id
                          join tasks on tasks.task_id = task_user.task_id;
        """)
        task = cur.fetchall()
        cur.close()
        conn.close()
        return task

    def fetch_user_task(self, name: str):
        conn, cur = connector()
        cur.execute("""SELECT
                            id,
                            user,
                            roles.role,
                            tasks.task_desc,
                            tasks.due_date
                        FROM
                            members
                            inner join roles ON roles.role_id = members.role
                            join task_user on task_user.user_id = members.id
                            join tasks on tasks.task_id = task_user.task_id
                        WHERE 
                            user=?
                """, (name, ))
        task = cur.fetchall()
        cur.close()
        conn.close()
        return task

    def fetch_roles(self):
        conn, cur = connector()
        cur.execute("""SELECT * FROM roles """)
        roles = cur.fetchall()
        cur.close()
        conn.close()
        return roles

    # for api access, mostly POST methods
    def add_member(self, user, role):
        conn, cur = connector()
        try:
            user_id = cur.execute("SELECT id FROM members WHERE user=?", (user,)).fetchone()[0]
        except TypeError:
            user_id = None
        try:
            role_id = cur.execute("SELECT role_id FROM roles WHERE role=?", (role,)).fetchone()[0]
        except TypeError:
            role_id = None

        if role_id is not None and user_id is None:
            try:
                cur.execute("""INSERT INTO members (user, role)
                                VALUES (?, ?)""",
                            (user, role_id, ))
                conn.commit()
                conn.close()
            except Exception:
                return 1
            return 0
        else:
            return 1

    def add_role(self, role):
        conn, cur = connector()
        try:
            role_id = cur.execute("SELECT role_id FROM roles WHERE role=?", (role,)).fetchone()[0]
        except TypeError:
            role_id = None

        if role_id is None:
            try:
                cur.execute("""INSERT INTO roles (role)
                                VALUES (?)""",
                            (role, ))
                conn.commit()
                conn.close()
            except Exception:
                return 1
            return 0
        return 1

    def add_task(self, task, due_date):
        conn, cur = connector()
        try:
            task_id = cur.execute("SELECT task_id FROM tasks WHERE task_desc=?", (task,)).fetchone()[0]
        except TypeError:
            task_id = None

        if task_id is None:
            try:
                cur.execute("""INSERT INTO tasks (task_desc, due_date)
                                VALUES (?, ?)""",
                            (task, due_date, ))
                conn.commit()
                conn.close()
            except Exception:
                return 1

            return 0
        return 1

    def assign_task(self, user, task):
        conn, cur = connector()
        try:
            user_id = cur.execute("SELECT id FROM members WHERE user=?", (user,)).fetchone()[0]
        except TypeError:
            user_id = None
        try:
            task_id = cur.execute("SELECT task_id FROM tasks WHERE task_desc=?", (task,)).fetchone()[0]
        except TypeError:
            task_id = None

        if task_id is not None and user_id is not None:
            try:
                cur.execute("""INSERT INTO task_user (user_id, task_id)
                                VALUES (?, ?)""",
                            (user_id, task_id))
                conn.commit()
                conn.close()
            except Exception:
                return 1
            return 0
        elif task_id is None and user_id is not None:
            return 2
        elif task_id is not None and user_id is None:
            return 3
        elif task_id is None and user_id is None:
            return 4
        return 1
