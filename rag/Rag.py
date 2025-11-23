from typing import List
from sentence_transformers import SentenceTransformer
import chromadb
import Config
from chromadb.api.models.Collection import Collection
from sentence_transformers import CrossEncoder
import os
from google import genai

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"


class Rag:
    def __init__(self, file_path: str, hf_token: str, embedding_model_name: str):
        self.file_path = file_path
        self.hf_token = hf_token
        self.embedding_model_name = embedding_model_name

    def __str__(self):
        return f"{self.file_path} - {self.hf_token}"

    def split_into_chunks(self) -> List[str]:
        """
        文章分段
        :return:
        """
        with open(self.file_path, "r", encoding="UTF-8") as file:
            content = file.read()
        return [x for x in content.split("\n\n")]

    def chunk_to_embed(self, chunk: str) -> List[float]:
        embedding_model = SentenceTransformer(self.embedding_model_name, token=self.hf_token, cache_folder="../models")
        embedding = embedding_model.encode(chunk)
        print(f"shape={embedding.shape}  维度={len(embedding)}   池化方法={embedding_model._modules['1']}")
        return embedding.tolist()

    def __chromadb_collection(self) -> Collection:
        chromadb_client = chromadb.EphemeralClient()
        # chromadb.PersistentClient("./chroma.db")
        return chromadb_client.get_or_create_collection(name="default")

    def save_embeddings(self, chunks: List[str], embeddings: List[List[float]]) -> None:
        chromadb_collection = self.__chromadb_collection()
        ids = [str(i) for i in range(len(chunks))]
        chromadb_collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids
        )

    def retrieve_fragment(self, query: str, top_k: int) -> List[str]:
        query_embedding = self.chunk_to_embed(query)
        results = self.__chromadb_collection().query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        return results['documents'][0]

    def re_rank(self, query_str: str, retrieve_chunks: List[str], top_k: int) -> List[str]:
        cross_encoder = CrossEncoder('cross-encoder/mmarco-mMiniLMv2-L12-H384-v1', cache_folder="../models")
        pairs = [(query_str, chunk) for chunk in retrieve_chunks]
        scores = cross_encoder.predict(pairs)
        chunk_with_score_list = [(chunk, score) for chunk, score in zip(retrieve_chunks, scores)]
        chunk_with_score_list.sort(key=lambda pair: pair[1], reverse=True)
        return [chunk for chunk, _ in chunk_with_score_list][:top_k]


    # 调用大模型生成
    def generate(self, query: str, chunks: List[str]) -> str:
        """
        :param str
        :param chunks 重排后的列表
        """
        google_client = genai.Client()
        prompt = f"""你是一位知识助手，请根据用户的问题和下列片段生成准确的回答。
        用户问题：{query}        
        相关片段：
        {"\n\n".join(chunks)}
        请基于上述内容作答，不要编造信息。"""
        response = google_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text



if __name__ == '__main__':
    properties = Config.all_config()
    rag = Rag("sample.md", properties['hf_hub_token'], properties['embedding_model_name'])
    print(rag)
    print("分片===================")
    # 分片
    sections = rag.split_into_chunks()
    for i, r in enumerate(sections):
        print(f"[{i}] {r}\n")
    # 向量化
    embeddings = [rag.chunk_to_embed(chunk) for chunk in sections]
    # 存储到向量数据库
    rag.save_embeddings(sections, embeddings)
    # 召回
    query = "为什么是藏在罐子里的爱？"
    retrieve_chunks = rag.retrieve_fragment(query, 5)
    print("召回================")
    for i, r in enumerate(retrieve_chunks):
        print(f"[{i}] {r}\n")
    print("重排================")
    final_result = rag.re_rank(query, retrieve_chunks, 3)
    for i, r in enumerate(final_result):
        print(f"[{i}] {r}\n")
