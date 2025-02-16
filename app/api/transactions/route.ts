import { NextResponse } from "next/server";

const NEXT_PUBLIC_ALPACA_URL = process.env.NEXT_PUBLIC_ALPACA_URL; // Use live API if needed

export async function POST(req: Request) {
  try {
    if (!process.env.NEXT_PUBLIC_ALPACA_API_KEY || !process.env.NEXT_PUBLIC_ALPACA_SECRET_KEY) {
      throw new Error("Alpaca API key or secret key not found");
    }
    if (!NEXT_PUBLIC_ALPACA_URL) {
      throw new Error("Alpaca URL not found");
    }

    const { api_key, private_key } = await req.json();

    const response = await fetch(`${NEXT_PUBLIC_ALPACA_URL}/account/activities`, {
      method: "GET",
      headers: {
        "APCA-API-KEY-ID": `${api_key}`,
        "APCA-API-SECRET-KEY": `${private_key}`,
      },
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status} ${response.statusText}`);
    }
    const data = await response.json();
    return NextResponse.json(data, { status: 200 });
  } catch (error: any) {
    console.error(`Error: ${error}`);
    return NextResponse.json({ message: error.message }, { status: 500 });
  }
}