import { promises as fs } from 'fs';
import path from 'path';
import { parse } from 'csv-parse/sync';

export async function GET() {
  const csvPath = path.join(process.cwd(), 'data', 'final_data.csv');
  const csvContent = await fs.readFile(csvPath, 'utf-8');
  const records = parse(csvContent, { columns: true, skip_empty_lines: true });
  return new Response(JSON.stringify(records), { headers: { 'Content-Type': 'application/json' } });
} 