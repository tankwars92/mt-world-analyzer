import os
import sqlite3
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Dict, List, Tuple
import numpy as np

@dataclass
class WorldStats:
    total_blocks: int
    underground_blocks: int
    generated_blocks: int
    map_size_mb: float
    block_distribution: Dict[Tuple[int, int], int]

class MinetestWorldAnalyzer:
    def __init__(self, world_path: str):
        self.world_path = world_path
        self.map_path = "map.sqlite"
        self.world_mt_path = "world.mt"
        
    def analyze_world(self) -> WorldStats:
        conn = sqlite3.connect(self.map_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM blocks")
        total_blocks = cursor.fetchone()[0]
        
        map_size_mb = os.path.getsize(self.map_path) / (1024 * 1024)
        
        players_path = os.path.join(self.world_path, "players")
        
        cursor.execute("SELECT pos FROM blocks")
        positions = cursor.fetchall()
        
        block_distribution = {}
        underground_blocks = 0
        generated_blocks = 0
        
        for (pos,) in positions:
            x, y, z = self._decode_position(pos)
            if y < 0:
                underground_blocks += 1
            
            xz = (x // 16, z // 16)
            block_distribution[xz] = block_distribution.get(xz, 0) + 1
        
        conn.close()
        
        return WorldStats(
            total_blocks=total_blocks,
            underground_blocks=underground_blocks,
            generated_blocks=generated_blocks,
            map_size_mb=map_size_mb,
            block_distribution=block_distribution
        )
    
    def visualize_world(self, stats: WorldStats):
        fig = plt.figure(figsize=(15, 10))
        
        ax1 = fig.add_subplot(121)
        self._plot_block_heatmap(stats.block_distribution, ax1)
        
        ax2 = fig.add_subplot(122)
        self._plot_block_distribution_pie(stats, ax2)
        
        plt.tight_layout()
        plt.savefig("world_analysis.png")
        plt.show()
        
    def _decode_position(self, pos: int) -> Tuple[int, int, int]:
        x = self._unsigned_to_signed(pos % 4096, 2048)
        pos = (pos - x) // 4096
        y = self._unsigned_to_signed(pos % 4096, 2048)
        pos = (pos - y) // 4096
        z = self._unsigned_to_signed(pos % 4096, 2048)
        return x, y, z
    
    def _unsigned_to_signed(self, i: int, max_positive: int) -> int:
        if i < max_positive:
            return i
        return i - 2 * max_positive
    
    def _plot_block_heatmap(self, distribution: Dict[Tuple[int, int], int], ax):
        if not distribution:
            return
        
        x_coords, z_coords = zip(*distribution.keys())
        x_min, x_max = min(x_coords), max(x_coords)
        z_min, z_max = min(z_coords), max(z_coords)
        
        width = x_max - x_min + 1
        height = z_max - z_min + 1
        
        heatmap = np.zeros((height, width))
        
        for (x, z), count in distribution.items():
            heatmap[z - z_min, x - x_min] = count
        
        im = ax.imshow(heatmap, cmap='hot', interpolation='nearest')
        ax.set_title('Распределение блоков в мире')
        ax.set_xlabel('X координата (чанки)')
        ax.set_ylabel('Z координата (чанки)')
        plt.colorbar(im, ax=ax)
    
    def _plot_block_distribution_pie(self, stats: WorldStats, ax):
        labels = ['Подземные', 'Наземные']
        sizes = [
            stats.underground_blocks,
            stats.total_blocks - stats.underground_blocks
        ]
        
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.set_title('Распределение блоков по высоте')

if __name__ == "__main__":
    analyzer = MinetestWorldAnalyzer("map.sqlite")
    stats = analyzer.analyze_world()
    analyzer.visualize_world(stats)
    
    print(f"Статистика мира:")
    print(f"Всего блоков: {stats.total_blocks}")
    print(f"Подземных блоков: {stats.underground_blocks}")
    print(f"Размер карты: {stats.map_size_mb:.2f} МБ")