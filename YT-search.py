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
        email = get_channel_email(channel_id)
        channels.append((channel_title, channel_url, email))

    return channels


def get_channel_email(channel_id):
    # 调用YouTube Data API获取频道的详细信息
    request = youtube.channels().list(
        part="snippet",
        id=channel_id
    )
    response = request.execute()

    # 提取频道的电子邮件信息（如果可用）
    email = None
    if "items" in response and len(response["items"]) > 0:
        channel_info = response["items"][0]
        if "snippet" in channel_info and "email" in channel_info["snippet"]:
            email = channel_info["snippet"]["email"]

    return email


def main():
    # Streamlit应用程序的主函数
    st.title("YouTube Channel Search")
    query = st.text_input("Enter a keyword to search on YouTube")
    if st.button("Search"):
        if query:
            channels = search_videos(query)
            st.subheader("Search Results")
            if channels:
                for channel_title, channel_url, email in channels:
                    st.write(f"- [{channel_title}]({channel_url})")
                    if email:
                        st.write(f"Email: {email}")
            else:
                st.write("No channels found.")


if __name__ == "__main__":
    main()
