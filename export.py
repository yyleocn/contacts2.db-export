import sqlite3

contactDBName = 'contacts2.db'
outputFileName = 'contacts.vcf'

outputFormat = """
BEGIN:VCARD
VERSION:3.0
N:;{name};;;
FN:{name}
{content}END:VCARD"""

if __name__ == '__main__':
    sqlCon = sqlite3.connect(contactDBName)
    sqlCur = sqlCon.cursor()
    contactList = list(sqlCur.execute('SELECT _id,name_raw_contact_id FROM contacts'))
    with open(outputFileName, 'w+', encoding='UTF-8') as fp:
        for row in contactList:
            data = {
                'name': '',
                'content': '',
            }
            for dataRec in sqlCur.execute(
                    'select _id,mimetype_id,data1,raw_contact_id from data where raw_contact_id=%s' % (row[0],)
            ):
                if (dataRec[1] == 7):
                    data['name'] = dataRec[2]
                if (dataRec[1] == 5):
                    data['content'] += 'TEL;TYPE=cell:%s\n' % (
                        str(dataRec[2]).replace(' ', '').replace('-', ''),
                    )
                if (dataRec[1] == 1):
                    data['content'] += 'EMAIL;TYPE=WORK:%s\n' % (dataRec[2],)
            resText = outputFormat.format(**data)
            # if not data['name']:
            #     print(data)
            if data['content'] and data['name']:
                fp.write(resText)
