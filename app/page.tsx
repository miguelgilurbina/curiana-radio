import type { Metadata } from "next";
import IntroDisco from "@/components/intro/IntroDisco";

export const metadata: Metadata = {
  alternates: { canonical: "/" },
};

// La puerta de la radio: la intro El Disco. Una vez por sesión; quien ya
// sintonizó pasa directo a la landing (/inicio). BRAND_MVP.md §9.
export default function Home() {
  return <IntroDisco />;
}
