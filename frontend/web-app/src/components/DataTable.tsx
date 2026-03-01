import React from 'react';

interface Column {
    key: string;
    label: string;
    render?: (value: any, row: any) => React.ReactNode;
}

interface DataTableProps {
    columns: Column[];
    data: any[];
    title?: string;
    emptyMessage?: string;
}

export default function DataTable({ columns, data, title, emptyMessage = 'No data available' }: DataTableProps) {
    return (
        <div className="glass-card overflow-hidden">
            {title && (
                <div className="px-5 py-4 border-b border-slate-700/50">
                    <h3 className="text-sm font-semibold text-slate-200">{title}</h3>
                </div>
            )}
            <div className="overflow-x-auto">
                <table className="w-full">
                    <thead>
                        <tr className="border-b border-slate-700/50">
                            {columns.map((col) => (
                                <th key={col.key} className="px-5 py-3 text-left text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                                    {col.label}
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800/50">
                        {data.length === 0 ? (
                            <tr>
                                <td colSpan={columns.length} className="px-5 py-8 text-center text-sm text-slate-500">
                                    {emptyMessage}
                                </td>
                            </tr>
                        ) : (
                            data.map((row, i) => (
                                <tr key={i} className="hover:bg-slate-800/30 transition-colors">
                                    {columns.map((col) => (
                                        <td key={col.key} className="px-5 py-3 text-sm text-slate-300">
                                            {col.render ? col.render(row[col.key], row) : row[col.key]}
                                        </td>
                                    ))}
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
