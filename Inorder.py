from manim import *
import numpy as np

class InorderWithPointer(Scene):
    def construct(self):
        # ১. সেটিংস্
        self.camera.background_color = BLACK
        
        # নোড এবং হাইলাইটের কিছু ধ্রুবক (constants)
        NODE_RADIUS = 0.4
        NORMAL_STROKE_WIDTH = 4
        POINTER_STROKE_WIDTH = 12 # পয়েন্টার হলে বর্ডার যত মোটা হবে
        
        NORMAL_COLOR = WHITE
        HIGHLIGHT_COLOR = YELLOW # কারেন্ট নোড বোঝাতে বর্ডারের রঙ
        PROCESSED_COLOR = GREEN  # প্রসেসড নোডের ব্যাকগ্রাউন্ড ফিল কালার

        # ২. ৩টি লেভেলের নোড পজিশন
        positions = {
            1: np.array([0, 2, 0]),     # Root
            2: np.array([-2, 0, 0]),    # Left child
            3: np.array([2, 0, 0]),     # Right child
            4: np.array([-3, -2, 0]),   # Left-Left
            5: np.array([-1, -2, 0]),   # Left-Right
            6: np.array([1, -2, 0]),    # Right-Left
            7: np.array([3, -2, 0])     # Right-Right
        }

        # ৩. নোড তৈরি করা (Circle + Text) - শুরুতে সব সাদা বর্ডার, কালো ফিল
        circles = {}
        texts = {}
        nodes_vgroup = VGroup()

        for i, pos in positions.items():
            circle = Circle(
                radius=NODE_RADIUS, 
                color=NORMAL_COLOR, 
                stroke_width=NORMAL_STROKE_WIDTH,
                fill_color=BLACK, 
                fill_opacity=1
            )
            text = Text(str(i), color=WHITE).scale(0.6)
            
            node = VGroup(circle, text)
            node.move_to(pos)
            
            circles[i] = circle # সার্কেলগুলোকে আলাদা ট্র‍্যাক করার জন্য
            texts[i] = text
            nodes_vgroup.add(node)

        # ৪. এজ কানেকশন তৈরি করা
        edge_pairs = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)]
        edges = {}
        for u, v in edge_pairs:
            vec = positions[v] - positions[u]
            unit_vec = vec / np.linalg.norm(vec)
            start = positions[u] + unit_vec * NODE_RADIUS
            end = positions[v] - unit_vec * NODE_RADIUS
            
            line = Line(start, end, color=WHITE, stroke_width=4)
            edges[(u, v)] = line
        
        edges_vgroup = VGroup(*edges.values())

        # ৫. শুরুতে পুরো ট্রি স্ক্রিনে দেখানো
        self.play(Create(edges_vgroup), run_time=1)
        self.play(Create(nodes_vgroup), run_time=1)
        self.wait(1)

        # ৬. হেল্পার ফাংশনসমূহ (অ্যানিমেশনের জন্য)
        
        # পয়েন্টার এক নোড থেকে অন্য নোডে নেওয়া (বর্ডার চেঞ্জ)
        def move_pointer(from_node, to_node, run_time=0.5):
            animations = []
            
            # আগের নোড স্বাভাবিক অবস্থায় ফেরানো
            if from_node:
                animations.append(circles[from_node].animate.set_stroke(
                    color=NORMAL_COLOR, width=NORMAL_STROKE_WIDTH
                ))
            
            # নতুন নোডকে পয়েন্টার দিয়ে হাইলাইট করা
            if to_node:
                animations.append(circles[to_node].animate.set_stroke(
                    color=HIGHLIGHT_COLOR, width=POINTER_STROKE_WIDTH
                ))
            
            if animations:
                self.play(*animations, run_time=run_time)

        # নোড প্রসেস করা (ব্যাকগ্রাউন্ড ফিল চেঞ্জ)
        def process_node(node_id):
            self.play(
                # ব্যাকগ্রাউন্ড সবুজ করা এবং টেক্সট সাদা রাখা
                circles[node_id].animate.set_fill(PROCESSED_COLOR, opacity=1),
                run_time=0.5
            )
            # প্রসেস করার পর একটু বাউন্স এফেক্ট দেওয়া
            self.play(
                circles[node_id].animate.scale(1.1),
                run_time=0.1
            )
            self.play(
                circles[node_id].animate.scale(1/1.1),
                run_time=0.1
            )

        # এজের কালার চেঞ্জ (হলুদ=কারেন্ট পাথ)
        def highlight_edge(u, v, is_active=True):
            edge_key = (u, v) if (u, v) in edges else (v, u)
            color = HIGHLIGHT_COLOR if is_active else WHITE
            self.play(edges[edge_key].animate.set_color(color), run_time=0.3)

        # --- Inorder Traversal অ্যানিমেশন শুরু (4 -> 2 -> 5 -> 1 -> 6 -> 3 -> 7) ---

        # শুরুতে ১ (Root) এ পয়েন্টার
        # আমরা ট্রাভার্সাল শুরু করব, কিন্তু প্রথম 'প্রসেস' করার জন্য ৪ এ যেতে হবে।
        circles[1].set_stroke(color=HIGHLIGHT_COLOR, width=POINTER_STROKE_WIDTH)
        self.wait(0.5)

        # ১. বামে যাও (1 -> 2)
        highlight_edge(1, 2)
        move_pointer(1, 2)
        
        # ২. বামে যাও (2 -> 4)
        highlight_edge(2, 4)
        move_pointer(2, 4)
        
        # ৩. প্রসেস ৪ (4 is processed) - BG পরিবর্তন
        process_node(4)
        
        # ৪. ৪ থেকে ব্যাকে যাও ২ তে (Backtracking)
        highlight_edge(2, 4, is_active=False)
        move_pointer(4, 2)
        
        # ৫. প্রসেস ২ (2 is processed) - BG পরিবর্তন
        process_node(2)
        
        # ৬. ডানে যাও (2 -> 5)
        highlight_edge(2, 5)
        move_pointer(2, 5)
        
        # ৭. প্রসেস ৫ (5 is processed) - BG পরিবর্তন
        process_node(5)
        
        # ৮. ৫ থেকে ব্যাকে যাও ১ তে (2 -> 1)
        highlight_edge(2, 5, is_active=False)
        highlight_edge(1, 2, is_active=False)
        move_pointer(5, 1) # সরাসরি 5 থেকে 1 এ মুভ করলাম ভিজ্যুয়াল Clarityর জন্য
        
        # ৯. প্রসেস ১ (Root is processed) - BG পরিবর্তন
        process_node(1)
        
        # ১০. ডানে যাও (1 -> 3)
        highlight_edge(1, 3)
        move_pointer(1, 3)
        
        # ১১. বামে যাও (3 -> 6)
        highlight_edge(3, 6)
        move_pointer(3, 6)
        
        # ১২. প্রসেস ৬ (6 is processed) - BG পরিবর্তন
        process_node(6)
        
        # ১৩. ৬ থেকে ব্যাকে যাও ৩ তে (3 -> 6)
        highlight_edge(3, 6, is_active=False)
        move_pointer(6, 3)
        
        # ১৪. প্রসেস ৩ (3 is processed) - BG পরিবর্তন
        process_node(3)
        
        # ১৫. ডানে যাও (3 -> 7)
        highlight_edge(3, 7)
        move_pointer(3, 7)
        
        # ১৬. প্রসেস ৭ (7 is processed) - BG পরিবর্তন
        process_node(7)

        # ১৭. ৭ থেকে ব্যাকে যাওয়া (3 -> 7, 1 -> 3) - সবার শেষে স্বাভাবিক অবস্থা
        highlight_edge(3, 7, is_active=False)
        highlight_edge(1, 3, is_active=False)
        
        # শেষ নোডের পয়েন্টার স্বাভাবিক করা
        self.play(circles[7].animate.set_stroke(
            color=NORMAL_COLOR, width=NORMAL_STROKE_WIDTH
        ), run_time=0.5)

        self.wait(2)