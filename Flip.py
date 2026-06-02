from manim import *
import numpy as np

class FlipBinaryTree2D(Scene):
    def setup(self):
        # ব্যাকগ্রাউন্ড কালার ডার্ক ব্লু সেট করা হলো
        self.camera.background_color = "#0B192C"

    # সেলিব্রেশন ইফেক্ট (সোয়াপ হওয়া নোডগুলোর ওপর)
    def play_celebration(self, target_nodes, num_particles=15):
        # GREEN_SCREEN এর বদলে GREEN ব্যবহার করা হলো
        colors = [YELLOW, RED, ORANGE, GREEN, PURPLE]
        all_animations = []
        all_particles = VGroup()
        
        # যতগুলো নোড সোয়াপ হয়েছে, সবার জন্য কনফেটি তৈরি করা
        for node in target_nodes:
            particles = VGroup(*[
                Dot(color=np.random.choice(colors), radius=0.06).move_to(node.get_center())
                for _ in range(num_particles)
            ])
            all_particles.add(particles)
            
            for particle in particles:
                dist = 0.8 + np.random.random() * 0.7
                angle = np.random.uniform(0, TAU)
                end_pos = particle.get_center() + dist * rotate_vector(RIGHT, angle)
                
                # পার্টিকলগুলো ছড়িয়ে পড়বে এবং ছোট হয়ে ভ্যানিশ হবে
                all_animations.append(
                    particle.animate(rate_func=smooth, run_time=0.8).move_to(end_pos).scale(0.01)
                )
        
        self.add(all_particles)
        self.play(*all_animations)
        self.remove(all_particles)

    def construct(self):
        # ১. টাইটেল
        title = Text("Binary Tree Flip", font_size=32, color=YELLOW)
        title.to_edge(UP)
        self.add(title)
        self.wait(1)

        # ২. নোড পজিশন
        pos = {
            1: np.array([0, 2, 0]),       # Root
            2: np.array([-2.5, 0, 0]),   # Level 1 Left
            3: np.array([2.5, 0, 0]),    # Level 1 Right
            4: np.array([-3.75, -2, 0]), # Level 2 Left-Left
            5: np.array([-1.25, -2, 0]), # Level 2 Left-Right
            6: np.array([1.25, -2, 0]),  # Level 2 Right-Left
            7: np.array([3.75, -2, 0]),  # Level 2 Right-Right
        }

        # ৩. নোড তৈরি (Circle এবং Text একসাথে VGroup করা হয়েছে)
        nodes = {}
        for i in range(1, 8):
            # সার্কেল
            c = Circle(radius=0.4, color="#4BC0C0", stroke_width=4, fill_opacity=0.9, fill_color="#1A2A40")
            # টেক্সট
            t = Text(str(i), font_size=24, color=WHITE)
            # VGroup করে একসাথে লকিং
            nodes[i] = VGroup(c, t)
            nodes[i].move_to(pos[i])

        # ৪. পেরিমিটার (Perimeter) থেকে এজ কানেকশন
        def get_connection(u, v):
            start = u.get_center()
            end = v.get_center()
            direction = (end - start) / np.linalg.norm(end - start)
            return Line(start + direction * 0.4, end - direction * 0.4, color=GRAY_B, stroke_width=3)

        initial_edges = VGroup(
            always_redraw(lambda: get_connection(nodes[1], nodes[2])),
            always_redraw(lambda: get_connection(nodes[1], nodes[3])),
            always_redraw(lambda: get_connection(nodes[2], nodes[4])),
            always_redraw(lambda: get_connection(nodes[2], nodes[5])),
            always_redraw(lambda: get_connection(nodes[3], nodes[6])),
            always_redraw(lambda: get_connection(nodes[3], nodes[7]))
        )

        all_nodes = VGroup(*[nodes[i] for i in range(1, 8)])
        self.play(FadeIn(all_nodes, lag_ratio=0.1), Create(initial_edges), run_time=2)
        self.wait(1)

        # --- ফেজ ১: লিফ লেভেল সোয়াপ ---
        
        def swap_pair(v1, v2, parent, speed=1.8, path_arc_sign=1):
            # v1[0] মানে হলো নোডের সার্কেলটি, যেন টেক্সটের কালার নষ্ট না হয়
            self.play(parent[0].animate.set_color(RED), run_time=0.5)

            # পেয়ার হাইলাইট ও বাউন্স
            self.play(
                v1[0].animate.set_color(YELLOW),
                v2[0].animate.set_color(YELLOW),
                v1.animate.scale(1.2), 
                v2.animate.scale(1.2),
                run_time=0.4
            )

            # গোল হয়ে সোয়াপ করা (Left <-> Right)
            v1_pos = v1.get_center()
            v2_pos = v2.get_center()
            self.play(
                v1.animate(path_arc=path_arc_sign * PI).move_to(v2_pos),
                v2.animate(path_arc=-path_arc_sign * PI).move_to(v1_pos),
                run_time=speed,
                rate_func=smooth
            )

            # কালার ও সাইজ রিসেট
            self.play(
                parent[0].animate.set_color("#4BC0C0"),
                v1[0].animate.set_color("#4BC0C0"),
                v2[0].animate.set_color("#4BC0C0"),
                v1.animate.scale(1/1.2),
                v2.animate.scale(1/1.2),
                run_time=0.4
            )
            # সফল সোয়াপের পর ঠিক ওই দুটি নোডের ওপর সেলিব্রেশন!
            self.play_celebration([v1, v2])

        # লিফ ১ সোয়াপ (4 এবং 5)
        swap_pair(nodes[4], nodes[5], nodes[2], path_arc_sign=1)
        self.wait(0.5)

        # লিফ ২ সোয়াপ (6 এবং 7)
        swap_pair(nodes[6], nodes[7], nodes[3], path_arc_sign=-1)
        self.wait(1)

        # --- ফেজ ২: রুট লেভেল সাব-ট্রি সোয়াপ ---

        # রুট মার্ক করা
        self.play(nodes[1][0].animate.set_color(RED))
        
        # সাব-ট্রি গ্রুপ করা
        l_subtree = VGroup(nodes[2], nodes[4], nodes[5])
        r_subtree = VGroup(nodes[3], nodes[6], nodes[7])

        # সাব-ট্রিগুলোর সার্কেল কালার চেঞ্জ এবং বাউন্স
        self.play(
            *[n[0].animate.set_color(YELLOW) for n in l_subtree],
            *[n[0].animate.set_color(YELLOW) for n in r_subtree],
            l_subtree.animate.scale(1.1),
            r_subtree.animate.scale(1.1),
            run_time=0.6
        )

        # পুরো সাব-ট্রি ফ্লিপ করা
        shift_vector = nodes[3].get_center() - nodes[2].get_center()
        self.play(
            l_subtree.animate(path_arc=PI).shift(shift_vector),
            r_subtree.animate(path_arc=-PI).shift(-shift_vector),
            run_time=2.5,
            rate_func=smooth
        )

        # ৫. ফাইনাল কালার রিসেট এবং সাব-ট্রির রুটগুলোর ওপর গ্র্যান্ড সেলিব্রেশন
        self.play(
            nodes[1][0].animate.set_color("#4BC0C0"),
            *[n[0].animate.set_color("#4BC0C0") for n in l_subtree],
            *[n[0].animate.set_color("#4BC0C0") for n in r_subtree],
            l_subtree.animate.scale(1/1.1),
            r_subtree.animate.scale(1/1.1),
            run_time=0.5
        )
        
        # ২ ও ৩ নম্বর নোড (যারা এখন নতুন পজিশনে) তাদের ওপর সেলিব্রেশন
        self.play_celebration([nodes[2], nodes[3]], num_particles=105)
        
    
        self.wait(3)