import os
import googleapiclient.discovery
import streamlit as st

# 从命令行参数或环境变量获取YouTube API密钥
API_KEY = st.text_input("Enter your YouTube API key", type="password")

# 创建YouTube Data API客户端
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)


def search_videos(query, max_results=10):
    # 调用YouTube Data API进行搜索
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="channel",
        maxResults=max_results
    )
    response = request.execute()

    # 解析搜索结果
    channels = []
    for item in response["items"]:
        channel_id = item["id"]["channelId"]
        channel_title = item["snippet"]["title"]
        channel_url = f"https://www.youtube.com/channel/{channel_id}"
        channels.append((channel_title, channel_url))

    return channels


def main():
    # Streamlit应用程序的主函数
    st.title("YouTube Channel Search")
    query = st.text_input("Enter a keyword to search on YouTube")
    if st.button("Search"):
        if query:
            channels = search_videos(query)
            st.subheader("Search Results")
            if channels:
                for channel_title, channel_url in channels:
                    st.write(f"- [{channel_title}]({channel_url})")
            else:
                st.write("No channels found.")


if __name__ == "__main__":
    main()
