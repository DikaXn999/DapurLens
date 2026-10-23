import { getFoods } from "@/lib/api";
import FoodExplorer from "@/components/FoodExplorer";

export const dynamic = "force-dynamic";

export default async function Home() {
  const foods = await getFoods();

  return (
    <main className="mx-auto w-full max-w-md md:max-w-3xl lg:max-w-6xl px-4 md:px-6">
      <FoodExplorer foods={foods} />
    </main>
  );
}
