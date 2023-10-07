import { faker } from '@faker-js/faker'
import axios from 'axios'

const API_LOCATION = "http://127.0.0.1:5030";
const HARDCODED_FILE_LOCATION = "http://127.0.0.1:5030/files";
const HARDCODED_FILE_LOCATION_REPLACE_REGEX = /^.*\/files/;

export type Data = {
  id: string
  tg_id: number
  tg_date: string
  tg_chat: string
  tg_chat_id: number
  tg_msg?: string
  tg_is_photo?: boolean
  tg_file_path?: string
}

export type Person = {
  firstName: string
  lastName: string
  age: number
  visits: number
  progress: number
  status: 'relationship' | 'complicated' | 'single'
  subRows?: Person[]
}

const range = (len: number) => {
  const arr = []
  for (let i = 0; i < len; i++) {
    arr.push(i)
  }
  return arr
}

const newPerson = (): Person => {
  return {
    firstName: faker.person.firstName(),
    lastName: faker.person.lastName(),
    age: faker.number.int(40),
    visits: faker.number.int(1000),
    progress: faker.number.int(100),
    status: faker.helpers.shuffle<Person['status']>([
      'relationship',
      'complicated',
      'single',
    ])[0]!,
  }
}

export function makeData(...lens: number[]) {
  const makeDataLevel = (depth = 0): Person[] => {
    const len = lens[depth]!
    return range(len).map((d): Person => {
      return {
        ...newPerson(),
        subRows: lens[depth + 1] ? makeDataLevel(depth + 1) : undefined,
      }
    })
  }

  return makeDataLevel()
}

// const data = makeData(10000)
const data =
    [
      {
        "id": "1",
        "tg_id": 123,
        "tg_date": "2023-10-07",
        "tg_chat": "Chat 1",
        "tg_chat_id": 456,
        "tg_msg": "Hello, world!",
        "tg_is_photo": true,
        "tg_file_path": "/path/to/file1"
      },
      {
        "id": "2",
        "tg_id": 789,
        "tg_date": "2023-10-08",
        "tg_chat": "Chat 2",
        "tg_chat_id": 101,
        "tg_msg": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum",
        "tg_is_photo": false,
      },
      {
        "id": "3",
        "tg_id": 456,
        "tg_date": "2023-10-09",
        "tg_chat": "Chat 3",
        "tg_chat_id": 303,
        "tg_msg": "Another message here.",
        "tg_is_photo": true,
        "tg_file_path": "/path/to/file3"
      }
    ]

export async function fetchData(options: {
  pageIndex: number,
  pageSize: number,
}) {
  // Simulate some network latency
  // await new Promise(r => setTimeout(r, 500))

  const config = {
    method: 'get',
    url: `${API_LOCATION}/tg_msgs_raw?page=${options.pageIndex}&per_page=${options.pageSize}`,
    headers: { }
  };

  const dataSec  = await axios(config)
      .catch(function (error) {
        console.log(error);
      });
  // console.log(JSON.stringify(dataSec.data));

  const dataToShow = dataSec.data.data.map(dataPoint => {
    let dataCopy = {...dataPoint};

    // console.log(`copy=${JSON.stringify(dataCopy)}`);
    if (dataCopy.hasOwnProperty('tg_file_path')) {
      let current =dataCopy['tg_file_path'][0];
      console.log(`current=${current}`);
      let resultRepl = current.replace(HARDCODED_FILE_LOCATION_REPLACE_REGEX, HARDCODED_FILE_LOCATION);
      console.log(`resultRepl =${resultRepl}`);
      console.log(`current2=${current}`);
      dataPoint['tg_file_path'] = resultRepl;
    }

    return dataPoint;

  });


  return {
    rows: dataToShow,
    pageCount: dataSec.data.page_count,
  }
}

