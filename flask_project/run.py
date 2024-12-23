from app import create_app

app = create_app()

if __name__ == "__main__":
    print(app.url_map)  # 등록된 모든 라우트 출력
    app.run(debug=True)
