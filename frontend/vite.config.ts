import { copyFileSync } from "node:fs";
import { join } from "node:path";
import { defineConfig, type Plugin } from "vite";
import react from "@vitejs/plugin-react";

const isGhPages = process.env.GITHUB_PAGES === "true";

function ghPagesSpaFallback(): Plugin {
  return {
    name: "gh-pages-spa-fallback",
    closeBundle() {
      const dist = join(__dirname, "dist");
      copyFileSync(join(dist, "index.html"), join(dist, "404.html"));
    },
  };
}

// https://vite.dev/config/
export default defineConfig({
  base: isGhPages ? "/VeriFi/" : "/",
  plugins: [react(), ...(isGhPages ? [ghPagesSpaFallback()] : [])],
  server: {
    proxy: {
      // Frontend-only workaround: proxy API calls to FastAPI without needing CORS changes.
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
