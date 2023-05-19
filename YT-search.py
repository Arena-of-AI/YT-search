import os
import googleapiclient.discovery
import streamlit as st

# 从命令行参数或环境变量获取YouTube API密钥
API_KEY = st.text_input("Enter your YouTube API key", type="password")

# 创建YouTube Data API客户端
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)


def search_videos(query, max_results=20):
    # 调用YouTube Data API进行搜索
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=max_results,
        order="viewCount"
    )
    response = request.execute()

    # 解析搜索结果
    channels = []
    for item in response["items"]:
        video_id = item["id"]["videoId"]
        channel_id = item["snippet"]["channelId"]
        video_title = item["snippet"]["title"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        channel_title, description, custom_links, email = get_channel_info(channel_id)
        channels.append((channel_title, video_title, channel_id, video_url, description, custom_links, email))

    return channels


def get_channel_info(channel_id):
    request = youtube.channels().list(
        part="snippet, brandingSettings",
        id=channel_id
    )
    response = request.execute()

    if "items" in response:
        channel = response["items"][0]
        title = channel["snippet"]["title"]
        description = channel["snippet"]["description"]
        custom_links = channel["brandingSettings"]["channel"].get("featuredChannelsUrls", [])
        email = channel["snippet"].get("email", "")
        return title, description, custom_links, email

    return None, None, None, None


def main():
    # Streamlit应用程序的主函数
    st.title("YouTube Channel Search")
    query = st.text_input("Enter a keyword to search on YouTube")
    if st.button("Search"):
        if query:
            channels = search_videos(query)
            st.subheader("Search Results")
            if channels:
                for channel_title, video_title, channel_id, video_url, description, custom_links, email in channels:
                    st.write(f"- Channel: [{channel_title}]({video_url})")
                    st.write(f"  Video: {video_title}")
                    st.write(f"  Description: {description}")
                    st.write(f"  Custom Links: {', '.join(custom_links)}")
                    st.write(f"  Email: {email}")
                    st.write("--------")
            else:
                st.write("No channels found.")


if __name__ == "__main__":
    main()
