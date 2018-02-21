class SqlBuilder():

    def __init__(self):
        self.__queryBuild = []


    def select(self, selectWhat):
        '''
        SqlBuilder().select('*')
        select('pid, user_id, user_name')
        '''

        self.__queryBuild.append('SELECT {}'.format(selectWhat))
        return self


    def selectDistinct(self, selectWhat):
        '''
        SqlBuilder().select('*')
        select('pid, user_id, user_name')
        '''

        self.__queryBuild.append('SELECT DISTINCT {}'.format(selectWhat))
        return self


    def fromTable(self, table):
        '''
        sql = SqlBuilder()
        sql.select('*').fromTable('category')
        => SELECT * FROM users

        sql.SqlBuilder().select('pid, user_id, user_name').fromTable('users').create()
        => SELECT pid, user_id, user_name FROM users
        '''

        self.__queryBuild.append('FROM {}'.format(table))
        return self


    def create(self):
        '''
        sql = SqlBuilder()
        sql.select('*').fromTable('users').create()
        => SELECT * FROM users
        will return sql string and will flush and clear the sqlbuilder object
        '''

        query = ' '.join(self.__queryBuild)
        self.__queryBuild.clear()
        return query


    def where(self, where):
        '''
        sql = SqlBuilder()
        sql.select('*').fromTable('users').where('users.pid=1').crate()
        => SELECT * FROM users WHERE users.id=1
        '''

        self.__queryBuild.append('WHERE {}'.format(where))
        return self


    def aNd(self, andWhere):
        '''
        sql = SqlBuilder()
        sql.select('*').fromTable('users').where('users.pid=1').aNd('users.name=\'{}\'.format('amru'))
        => SELECT * FROM users WHERE users.id=1 AND name='amru'
        '''

        self.__queryBuild.append('AND {}'.format(andWhere))
        return self


    def oR(self, orWhere):
        '''
        sql = SqlBuilder()
        sql.select('*').fromTable('users').where('users.pid=1').oR('users.name=\'{}\''.format('amru'))
        => SELECT * FROM users WHERE users.id=1 OR name='amru'
        '''

        self.__queryBuild.append('OR {}'.format(orWhere))
        return self


    def inSelect(self, inSelect):
        '''
        sql = SqlBuilder()
        selectJob = sql.select('job.uid').fromTable('job').where('job.id=1').create()
        sql.select('*').fromTable('users').where('users.id').inSelect(selectJob).create()
        => SELECT * FROM users WHERE users.id IN (SELECT job.uid FROM job WHERE job.id=1)
        '''

        self.__queryBuild.append('IN ({})'.format(inSelect))
        return self


    def like(self, like):
        '''
        sql = SqlBuilder()
        selectJob = sql.select('job.uid').fromTable('job').where('job.name').like('\'{}\''.format('ngetik')).create()
        sql.select('*').fromTable('users').where('users.id').inSelect(selectJob).create()
        => SELECT * FROM users WHERE users.id IN (SELECT job.uid FROM job WHERE job.name LIKE 'ngetik')
        '''

        self.__queryBuild.append('LIKE {}'.format(like))
        return self


    def notLike(self, notLike):
        '''
        sql = SqlBuilder()
        selectJob = sql.select('job.uid').fromTable('job').where('job.name').notLike('\'{}\''.format('ngetik')).create()
        sql.select('*').fromTable('users').where('users.id').inSelect(selectJob).create()
        => SELECT * FROM users WHERE users.id IN (SELECT job.uid FROM job WHERE job.name NOT LIKE 'ngetik')
        '''

        self.__queryBuild.append('NOT LIKE {}'.format(notLike))
        return self


    def orderByDesc(self, orderBy):
        '''
        sql = SqlBuilder()
        selectJob = sql.select('job.uid').fromTable('job').where('job.name').notLike('\'{}\''.format('ngetik')).create()
        sql.select('*').fromTable('users').where('users.id').inSelect(selectJob).orderByDesc('users.name, users.id').create()
        => SELECT * FROM users WHERE users.id IN (SELECT job.uid FROM job WHERE job.name NOT LIKE 'ngetik') ORDER BY sers.name, users.id DESC
        '''

        self.__queryBuild.append('ORDER BY {} DESC'.format(orderBy))
        return self

    
    def orderByAsc(self, orderBy):
        '''
        sql = SqlBuilder()
        selectJob = sql.select('job.uid').fromTable('job').where('job.name').notLike('\'{}\''.format('ngetik')).create()
        sql.select('*').fromTable('users').where('users.id').inSelect(selectJob).orderByAsc('users.name, users.id').create()
        => SELECT * FROM users WHERE users.id IN (SELECT job.uid FROM job WHERE job.name NOT LIKE 'ngetik') ORDER BY sers.name, users.id ASC
        '''

        self.__queryBuild.append('ORDER BY {} ASC'.format(orderBy))
        return self


    def limit(self, limit):
        '''
        sql = SqlBuilder()
        selectJob = sql.select('job.uid').fromTable('job').where('job.name').notLike('\'{}\''.format('ngetik')).create()
        sql.select('*').fromTable('users').where('users.id').inSelect(selectJob).orderByAsc('users.name, users.id').limit(1).create()
        => SELECT * FROM users WHERE users.id IN (SELECT job.uid FROM job WHERE job.name NOT LIKE 'ngetik') ORDER BY sers.name, users.id ASC LIMIT 1
        '''

        self.__queryBuild.append('LIMIT {}'.format(limit))
        return self


    def limitWithOffset(self, limit, offset):
        '''
        sql = SqlBuilder()
        selectJob = sql.select('job.uid').fromTable('job').where('job.name').notLike('\'{}\''.format('ngetik')).create()
        sql.select('*').fromTable('users').where('users.id').inSelect(selectJob).orderByAsc('users.name, users.id').limitWithOffset(1, 0).create()
        => SELECT * FROM users WHERE users.id IN (SELECT job.uid FROM job WHERE job.name NOT LIKE 'ngetik') ORDER BY sers.name, users.id ASC LIMIT 1 OFFSET 0
        '''

        self.__queryBuild.append('LIMIT {} OFFSET {}'.format(limit, offset))
        return self


    def groupBy(self, groupBy):
        '''
        sql = SqlBuilder()
        sql.select('COUNT(job.uid) AS total_job, job.uid').fromTable('job').groupBy('job.uid').create()
        => SELECT COUNT(job.uid) AS total_job FROM job GROUP BY job.uid
        '''

        self.__queryBuild.append('GROUP BY {}'.format(groupBy))
        return self


    def innerJoin(self, table, innerJoinOn):
        '''
        sql = SqlBuilder()
        sql.select('users.name, job.name, users.id').fromTable('job').innerJoin('users', 'users.id=job.uid').create()
        => SELECT users.name, job.name, users.id FROM job INNER JOIN users ON users.id=job.uid
        '''

        self.__queryBuild.append('INNER JOIN {} ON {}'.format(table, innerJoinOn))
        return self


    def join(self, table, joinOn):
        '''
        sql = SqlBuilder()
        sql.select('users.name, job.name, users.id').fromTable('job').Join('users', 'users.id=job.uid').create()
        => SELECT users.name, job.name, users.id FROM job JOIN users ON users.id=job.uid
        '''

        self.__queryBuild.append('JOIN {} ON {}'.format(table, joinOn))
        return self


    def leftJoin(self, table, leftJoinOn):
        '''
        sql = SqlBuilder()
        sql.select('users.name, job.name, users.id').fromTable('job').leftJoin('users', 'users.id=job.uid').create()
        => SELECT users.name, job.name, users.id FROM job LEFT JOIN users ON users.id=job.uid
        '''

        self.__queryBuild.append('LEFT JOIN {} ON {}'.format(table, leftJoinOn))
        return self


    def rightJoin(self, table, rightJoinOn):
        '''
        sql = SqlBuilder()
        sql.select('users.name, job.name, users.id').fromTable('job').rightJoin('users', 'users.id=job.uid').create()
        => SELECT users.name, job.name, users.id FROM job RIGHT JOIN users ON users.id=job.uid
        '''

        self.__queryBuild.append('RIGHT JOIN {} ON {}'.format(table, rightJoinOn))
        return self


    def insert(self, table, column, values):
        '''
        sql = SqlBuilder()
        sql.insert('users', ('a', 'b'), (1, 'yes')).create()
        => INSERT INTO users (a,b) VALUES (1, 'yes')

        for insert multiple values
        sql.insert('users', ('a', 'b'), ((1, '3'), (1, '6'), (1, '8'))).create()
        => INSERT INTO users (a,b,c) VALUES (1,2,'yes'),(1,2,'yes')
        '''

        valuesToInsert = ''
        if len(values) and type(values[0]) == tuple:
            valuesList = []
            for insertValues in values:
                valuesList.append('({})'.format(', '.join(['\'{}\''.format(item) if type(item) == str else str(item) for item in insertValues])))

            valuesToInsert = ', '.join(valuesList)

        else:
            valuesToInsert = ', '.join(['\'{}\''.format(item) if type(item) == str else str(item) for item in values])

        self.__queryBuild.append('INSERT INTO {} ({}) VALUES {}'.format(table, ', '.join(column), valuesToInsert))
        return self


    def update(self, table, column, values):
        '''
        sql = SqlBuilder()
        sql.update('users', ('a', 'b'), (1, 'yes')).create()
        => UPDATE users SET a = 1, b = 'yes'
        '''

        updateValues = []
        for i in range(0, len(column)):
            updateValues.append('{} = {}'.format(column[i], '\'{}\''.format(values[i]) if type(values[i]) == str else str(values[i])))

        self.__queryBuild.append('UPDATE {} SET {}'.format(table, ', '.join(updateValues)))
        return self


    def delete(self, table):
        '''
        sql = SqlBuilder()
        sql.delete('users').where('uid=1')
        => DELETE FROM users WHERE uid=1
        '''

        self.__queryBuild.append('DELETE FROM {}'.format(table))
        return self
        