def create_study_plan():
    print("📚 Function Called: create_study_plan()")
    print("Your study plan:")
    print("1. Python Basics - 30 minutes")
    print("2. Functions - 30 minutes")
    print("3. Practice Questions - 30 minutes")


def suggest_break():
    print("☕ Function Called: suggest_break()")
    print("Take a 15-minute break and relax.")


def explain_topic():
    print("📖 Function Called: explain_topic()")
    print("AI will explain the requested topic.")


def student_agent(question):

    question = question.lower()

    # Agent decision-making
    if "exam" in question or "study" in question:
        decision = "create_study_plan"

    elif "tired" in question or "break" in question:
        decision = "suggest_break"

    else:
        decision = "explain_topic"

    print("\n🤖 Agent Decision:", decision)

    # Function calling
    if decision == "create_study_plan":
        create_study_plan()

    elif decision == "suggest_break":
        suggest_break()

    elif decision == "explain_topic":
        explain_topic()


question = input("👨‍🎓 Ask your question: ")

student_agent(question)