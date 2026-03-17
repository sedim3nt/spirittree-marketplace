// SpiritTree Marketplace — Supabase Auth
const SUPABASE_URL = 'https://gnhmveamzymuxlsymsuw.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImduaG12ZWFtenltdXhsc3ltc3V3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM1MzcwMjEsImV4cCI6MjA4OTExMzAyMX0.cliTxwWBMJXP6U-B-BtFkaUAY857D819f4ekXbkRgpY';

// Initialize Supabase client (loaded via CDN)
const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Auth state management
const AUTH = {
  user: null,

  async init() {
    const { data: { session } } = await supabase.auth.getSession();
    if (session) {
      this.user = session.user;
      this.updateUI();
    }
    // Listen for auth changes
    supabase.auth.onAuthStateChange((event, session) => {
      this.user = session?.user || null;
      this.updateUI();
    });
  },

  async signUp(email, password) {
    const { data, error } = await supabase.auth.signUp({ email, password });
    if (error) throw error;
    return data;
  },

  async signIn(email, password) {
    const { data, error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) throw error;
    return data;
  },

  async signOut() {
    const { error } = await supabase.auth.signOut();
    if (error) throw error;
    this.user = null;
    this.updateUI();
  },

  async resetPassword(email) {
    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: 'https://agentorchard.dev/reset-password.html'
    });
    if (error) throw error;
  },

  updateUI() {
    // Update nav login/logout links
    document.querySelectorAll('.nav-auth').forEach(el => {
      if (this.user) {
        el.innerHTML = `<a href="account.html" class="nav-login" style="border-color:var(--tide-600);color:var(--tide-600)">Account</a>`;
      } else {
        el.innerHTML = `<a href="login.html" class="nav-login">Login / Sign Up</a>`;
      }
    });
  }
};

// Auto-init on load
document.addEventListener('DOMContentLoaded', () => AUTH.init());
