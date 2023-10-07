import React from 'react'
import ReactDOM from 'react-dom/client'

import { QueryClient, QueryClientProvider, useQuery } from 'react-query'

import './index.css'

import {
  PaginationState,
  useReactTable,
  getCoreRowModel,
  ColumnDef,
  flexRender,
} from '@tanstack/react-table'

//

import { fetchData, Person, Data } from './fetchData'

const queryClient = new QueryClient()

function App() {
  const rerender = React.useReducer(() => ({}), {})[1]

  const DEBUG_MODE = true;
  let debugModeData1 = null;
  let debugModeData2 = null;


  const columns = React.useMemo<ColumnDef<Data>[]>(
    () => [
      {
        accessorKey: 'id',
        header: () => <span>id</span>,
      },
      {
        accessorKey: 'tg_id',
        header: () => <span>tg_id</span>,
      },
      {
        accessorKey: 'tg_date',
        header: () => <span>tg_date</span>,
      },
      {
        accessorKey: 'tg_chat',
        header: () => <span>tg_chat</span>,
      },
      {
        accessorKey: 'tg_chat_id',
        header: () => <span>tg_chat_id</span>,
      },
      {
        accessorKey: 'tg_msg',
        header: () => <span>tg_msg</span>,
      },
      {
        accessorKey: 'tg_is_photo',
        header: () => <span>tg_is_photo</span>,
      },
      {
        accessorKey: 'tg_file_path',
        header: () => <span>tg_file_path</span>,
        cell: info => <a href="url">{info.getValue()}</a>
      },
    ],
    []
  )

  const [{ pageIndex, pageSize }, setPagination] =
    React.useState<PaginationState>({
      pageIndex: 0,
      pageSize: 10,
    })

  const fetchDataOptions = {
    pageIndex,
    pageSize,
  }

  const dataQuery = useQuery(
    ['data', fetchDataOptions],
    () => fetchData(fetchDataOptions),
    { keepPreviousData: true }
  )

  const defaultData = React.useMemo(() => [], [])

  const pagination = React.useMemo(
    () => ({
      pageIndex,
      pageSize,
    }),
    [pageIndex, pageSize]
  )

  const table = useReactTable({
    data: dataQuery.data?.rows ?? defaultData,
    columns,
    pageCount: dataQuery.data?.pageCount ?? -1,
    state: {
      pagination,
    },
    onPaginationChange: setPagination,
    getCoreRowModel: getCoreRowModel(),
    manualPagination: true,
    // getPaginationRowModel: getPaginationRowModel(), // If only doing manual pagination, you don't need this
    debugTable: true,
  })


  if (DEBUG_MODE)
  {
    debugModeData1 = (
        <div>
          <button onClick={() => rerender()}>Force Rerender</button>
        </div>
    )
    debugModeData2 = <pre>{JSON.stringify(pagination, null, 2)}</pre>

  }

  return (
    <div className="p-2">
      <div className="h-2" />
      <table>
        <thead>
          {table.getHeaderGroups().map(headerGroup => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map(header => {
                return (
                  <th key={header.id} colSpan={header.colSpan}>
                    {header.isPlaceholder ? null : (
                      <div>
                        {flexRender(
                          header.column.columnDef.header,
                          header.getContext()
                        )}
                      </div>
                    )}
                  </th>
                )
              })}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map(row => {
            return (
              <tr key={row.id}>
                {row.getVisibleCells().map(cell => {
                  return (
                    <td key={cell.id}>
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext()
                      )}
                    </td>
                  )
                })}
              </tr>
            )
          })}
        </tbody>
      </table>
      <div className="h-2" />
      <div className="flex items-center gap-2">
        <button
          className="border rounded p-1"
          onClick={() => table.setPageIndex(0)}
          disabled={!table.getCanPreviousPage()}
        >
          {'<<'}
        </button>
        <button
          className="border rounded p-1"
          onClick={() => table.previousPage()}
          disabled={!table.getCanPreviousPage()}
        >
          {'<'}
        </button>
        <button
          className="border rounded p-1"
          onClick={() => table.nextPage()}
          disabled={!table.getCanNextPage()}
        >
          {'>'}
        </button>
        <button
          className="border rounded p-1"
          onClick={() => table.setPageIndex(table.getPageCount() - 1)}
          disabled={!table.getCanNextPage()}
        >
          {'>>'}
        </button>
        <span className="flex items-center gap-1">
          <div>Page</div>
          <strong>
            {table.getState().pagination.pageIndex + 1} of{' '}
            {table.getPageCount()}
          </strong>
        </span>
        <span className="flex items-center gap-1">
          | Go to page:
          <input
            type="number"
            defaultValue={table.getState().pagination.pageIndex + 1}
            onChange={e => {
              const page = e.target.value ? Number(e.target.value) - 1 : 0
              table.setPageIndex(page)
            }}
            className="border p-1 rounded w-16"
          />
        </span>
        <select
          value={table.getState().pagination.pageSize}
          onChange={e => {
            table.setPageSize(Number(e.target.value))
          }}
        >
          {[1, 10, 20, 30, 40, 50].map(pageSize => (
            <option key={pageSize} value={pageSize}>
              Show {pageSize}
            </option>
          ))}
        </select>
        {dataQuery.isFetching ? 'Loading...' : null}
      </div>
      <div>{table.getRowModel().rows.length} Rows</div>
      {debugModeData1}
      {debugModeData2}
    </div>
  )
}

const rootElement = document.getElementById('root')
if (!rootElement) throw new Error('Failed to find the root element')

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>
)
