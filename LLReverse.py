from manim import *
import numpy as np

class ReverseLinkedList(Scene):
    def construct(self):
        # ১. সেটিংস্
        self.camera.background_color = BLACK
        
        NODE_RADIUS = 0.4
        NORMAL_STROKE = 4
        HIGHLIGHT_STROKE = 8
        
        # থিম ও সাইজ
        THICK_ARROW_STROKE = 10
        NORMAL_COLOR = WHITE
        CURR_COLOR = YELLOW
        PROCESSED_COLOR = BLUE  # পিওর ব্লু থিম

        # ২. নোড ও NULL এর প্রাথমিক পজিশন (পারফেক্ট সেন্টারড স্পেসিং)
        positions = {
            'null_left': np.array([-5.5, 0, 0]),
            1: np.array([-3.3, 0, 0]),
            2: np.array([-1.1, 0, 0]),
            3: np.array([1.1, 0, 0]),
            4: np.array([3.3, 0, 0]),
            'null_right': np.array([5.5, 0, 0])
        }

        # ৩. নোড এবং NULL টেক্সট তৈরি
        nodes = {}
        circles = {}
        for i in range(1, 5):
            c = Circle(radius=NODE_RADIUS, color=NORMAL_COLOR, stroke_width=NORMAL_STROKE, fill_color=BLACK, fill_opacity=1)
            t = Text(str(i), font_size=24, color=WHITE)
            nodes[i] = VGroup(c, t).move_to(positions[i])
            circles[i] = c

        null_left_text = Text("NULL", font_size=22, color=GRAY).move_to(positions['null_left'])
        null_right_text = Text("NULL", font_size=22, color=GRAY).move_to(positions['null_right'])

        def get_target_mobj(id_or_pos):
            if id_or_pos == 'null_left': return null_left_text
            if id_or_pos == 'null_right': return null_right_text
            return nodes[id_or_pos]

        # ৪. ডাইনামিক অ্যারো ফাংশন
        def get_dynamic_arrow(m1, m2, color=WHITE):
            return Arrow(
                m1.get_center(), 
                m2.get_center(), 
                buff=NODE_RADIUS + 0.15, 
                color=color, 
                stroke_width=THICK_ARROW_STROKE, 
                max_tip_length_to_length_ratio=0.15
            )

        fwd_arrows = {
            1: always_redraw(lambda: get_dynamic_arrow(nodes[1], nodes[2])),
            2: always_redraw(lambda: get_dynamic_arrow(nodes[2], nodes[3])),
            3: always_redraw(lambda: get_dynamic_arrow(nodes[3], nodes[4])),
            4: always_redraw(lambda: get_dynamic_arrow(nodes[4], null_right_text))
        }

        # স্ক্রিনে প্রাথমিক লিস্ট দেখানো
        self.play(FadeIn(null_left_text), FadeIn(null_right_text), run_time=1)
        self.play(
            *[FadeIn(nodes[i]) for i in range(1, 5)],
            *[GrowArrow(fwd_arrows[i]) for i in range(1, 5)],
            run_time=1.5
        )
        self.wait(0.5)

        # ৫. গর্জিয়াস ও মোটা পয়েন্টার (হোয়াইট বোল্ড অ্যারো)
        def create_pointer(label_text, text_color, is_top=False):
            txt = Text(label_text, font_size=22, color=text_color)
            if is_top:
                arr = Arrow(UP * 0.8, ORIGIN, color=WHITE, stroke_width=14, max_tip_length_to_length_ratio=0.25, buff=0)
                return VGroup(txt, arr).arrange(DOWN, buff=0.15)
            else:
                arr = Arrow(DOWN * 0.8, ORIGIN, color=WHITE, stroke_width=14, max_tip_length_to_length_ratio=0.25, buff=0)
                return VGroup(arr, txt).arrange(DOWN, buff=0.15)

        prev_ptr = create_pointer("prev", RED, is_top=False).next_to(null_left_text, DOWN, buff=0.2)
        curr_ptr = create_pointer("curr", YELLOW, is_top=False).next_to(nodes[1], DOWN, buff=0.2)
        nxt_ptr = create_pointer("nxt", GREEN, is_top=True).next_to(nodes[1], UP, buff=0.2)

        self.play(
            FadeIn(prev_ptr, shift=RIGHT * 0.5), 
            FadeIn(curr_ptr, shift=UP * 0.5),    
            FadeIn(nxt_ptr, shift=DOWN * 0.5),   
            run_time=1.2,
            rate_func=rate_functions.smooth
        )
        self.wait(1)

        # ৬. রিভার্স করার কোর লজিক
        def reverse_step(curr_id, next_id):
            target_curr = nodes[curr_id]
            target_nxt = get_target_mobj(next_id)
            
            prev_id = curr_id - 1 if curr_id > 1 else 'null_left'
            target_prev = get_target_mobj(prev_id)

            self.play(circles[curr_id].animate.set_stroke(color=CURR_COLOR, width=HIGHLIGHT_STROKE), run_time=0.4)

            self.play(nxt_ptr.animate.next_to(target_nxt, UP, buff=0.2), run_time=0.6)

            # ক) অ্যানিমেশনের জন্য প্রথমে একটি স্ট্যাটিক ব্যাকওয়ার্ড অ্যারো তৈরি করি
            backward_arrow_static = get_dynamic_arrow(target_curr, target_prev, color=PROCESSED_COLOR)
            
            # খ) ফরোয়ার্ড অ্যারোর আপডেটার বন্ধ করি যেন ট্র্যান্সফর্মে কোনো গ্লিচ না হয়
            fwd_arrows[curr_id].clear_updaters()
            
            # গ) ReplacementTransform এর ম্যাজিক—ডানমুখী তীরটি চোখের সামনেই ঘুরে বামমুখী তীরে রূপান্তরিত হবে
            self.play(
                ReplacementTransform(fwd_arrows[curr_id], backward_arrow_static),
                run_time=0.8
            )

            # ঘ) ট্র্যান্সফর্ম শেষ হওয়া মাত্র এটিকে আবার ডাইনামিক (always_redraw) করে দিই 
            # যাতে একদম শেষে নোডগুলো গোল হয়ে ঘোরার সময় তীরগুলোও সাথে ঘোরে
            backward_arrow_dynamic = always_redraw(
                lambda c=target_curr, p=target_prev: get_dynamic_arrow(c, p, color=PROCESSED_COLOR)
            )
            self.remove(backward_arrow_static)
            self.add(backward_arrow_dynamic)

            # নোড প্রসেসড (পিওর ব্লু ফিল ও সেলিব্রেশন)
            self.play(
                circles[curr_id].animate.set_fill(PROCESSED_COLOR, opacity=1).set_stroke(color=NORMAL_COLOR, width=NORMAL_STROKE),
                Flash(circles[curr_id], color=BLUE, flash_radius=0.7, num_lines=14, stroke_width=4),
                run_time=0.5
            )

            # prev এবং curr শিফট
            self.play(
                prev_ptr.animate.next_to(target_curr, DOWN, buff=0.2),
                curr_ptr.animate.next_to(target_nxt, DOWN, buff=0.2),
                run_time=0.6
            )
            self.wait(0.3)

        # --- Iterations ---
        reverse_step(curr_id=1, next_id=2)
        reverse_step(curr_id=2, next_id=3)
        reverse_step(curr_id=3, next_id=4)
        reverse_step(curr_id=4, next_id='null_right')

        # ৭. Head ডিক্লেয়ার করা
        self.play(FadeOut(curr_ptr), FadeOut(nxt_ptr), FadeOut(null_right_text), run_time=0.8)
        
        head_label = Text("Head", font_size=24, color=PROCESSED_COLOR).next_to(nodes[4], UP, buff=0.3)
        self.play(
            Transform(prev_ptr, head_label),
            nodes[4].animate.scale(1.2),
            run_time=0.8
        )
        self.play(nodes[4].animate.scale(1/1.2), run_time=0.3)
        self.wait(1)

        # ৮. ফাইনাল অ্যানিমেশন: Left-to-Right সুন্দর এরেঞ্জমেন্ট
        final_positions = {
            4: np.array([-4.4, 0, 0]),
            3: np.array([-2.2, 0, 0]),
            2: np.array([0.0, 0, 0]),
            1: np.array([2.2, 0, 0]),
            'null_left': np.array([4.4, 0, 0])
        }

        prev_ptr.add_updater(lambda m: m.next_to(nodes[4], UP, buff=0.3))

        self.play(
            nodes[4].animate(path_arc=PI/1.5).move_to(final_positions[4]),
            nodes[3].animate(path_arc=PI/1.5).move_to(final_positions[3]),
            nodes[2].animate(path_arc=PI/1.5).move_to(final_positions[2]),
            nodes[1].animate(path_arc=PI/1.5).move_to(final_positions[1]),
            null_left_text.animate(path_arc=PI/1.5).move_to(final_positions['null_left']),
            run_time=2.5,
            rate_func=rate_functions.ease_in_out_sine
        )
        
        prev_ptr.clear_updaters()
        
        complete_label = Text("List Reversed Successfully!", font_size=28, color=BLUE).to_edge(DOWN)
        self.play(Write(complete_label))
        self.wait(3)