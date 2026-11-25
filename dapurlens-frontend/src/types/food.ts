export type FoodTag = "viral" | "daerah" | "western";

export interface Food {
  slug: string;
  name: string;
  region: string;
  tags: FoodTag[];
  emoji: string;
  description: string;
  gradientFrom: string;
  gradientTo: string;
  ingredients: string[];
  steps: string[];
}

// Data yang dikirim form saat membuat/mengubah resep. Slug dibuat backend,
// sedangkan emoji dan warna gradien dikirim dari form.
export type FoodInput = Omit<Food, "slug">;

export interface RecognitionCandidate {
  slug: string;
  name: string;
  confidence: number;
}

export interface RecognitionResult {
  matched: boolean;
  food: Food | null;
  confidence: number;
  candidates: RecognitionCandidate[];
  message: string;
  // Sisa jatah pindai gratis; hanya terisi untuk guest (null = user login, tanpa batas).
  guestRemaining: number | null;
}

