// User Types
export interface User {
  id: number;
  username: string;
  email: string;
  roles: string[];
  foto_perfil?: string | null;
}

export interface AuthResponse {
  refresh: string;
  access: string;
}

// Plan Types
export interface Exercise {
  id: number;
  nombre: string;
  grupo_muscular: string;
  descripcion: string;
  imagen_url: string;
  video_url: string;
  equipo: string;
  dificultad: string;
}

export interface RoutineExercise {
  id: number;
  ejercicio: Exercise;
  repeticiones: number;
  series: number;
  peso_sugerido: number | null;
  descanso_segundos: number;
  orden: number;
  observaciones: string | null;
}

export interface Routine {
  id: number;
  dia: number;
  tipo: 'entrenamiento' | 'descanso';
  fecha: string;
  observaciones: string | null;
  ejercicios: RoutineExercise[];
  realizada?: boolean;
  fecha_realizacion?: string;
}

export interface TrainingPlan {
  id: number;
  usuario: number;
  fecha_inicio: string;
  fecha_fin: string | null;
  objetivo: string;
  rutinas: Routine[];
}

// Conversation Types
export interface Conversation {
  id: number;
  usuario: number;
  plan: number;
  estado: string;
  mensajes: Message[];
}

export interface Message {
  id: number;
  tipo: 'sistema' | 'usuario';
  contenido: string;
  timestamp: string;
}

// Progress Types
export interface Progress {
  id: number;
  usuario: number;
  fecha: string;
  peso: number;
  medidas: {
    pecho: number;
    cintura: number;
    cadera: number;
  };
  energia: number;
  observaciones: string;
  fotos: string[];
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T;
} 