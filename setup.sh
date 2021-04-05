mkdir -p ~/.streamlit/

echo "[server]
headless = true
port = .listen(process.env.PORT || 5000)
enableCORS = false
" > ~/.streamlit/config.toml
