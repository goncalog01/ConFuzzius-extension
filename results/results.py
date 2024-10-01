import sys, os, tarfile, json, statistics

for metric_dir in os.listdir(sys.argv[1]):
    if not os.path.isdir(sys.argv[1] + "/" + metric_dir):
        continue
    instruction_coverage = list()
    branch_coverage = list()
    time_max_instruction_coverage = list()
    time_max_branch_coverage = list()
    time_bug = list()
    total_transaction_bug = list()
    unique_transactions_bug = list()
    transactions_per_second = list()
    percentage_unique_transactions = list()
    memory_consumption = list()
    execution_time = list()
    total_errors = 0

    fw = open(sys.argv[1] + "/" + metric_dir + "/results.txt", "w")
    fw.write("----- Errors -----\n")

    for contract_dir in os.listdir(sys.argv[1] + "/" + metric_dir):
        results_dir = sys.argv[1] + "/" + metric_dir + "/" + contract_dir
        if not os.path.isdir(results_dir):
            continue
        tar_path = results_dir + "/result.tar"
        if not os.path.isfile(tar_path):
            fw.write("{} - Execution error\n".format(contract_dir))
            continue
        tar = tarfile.open(tar_path)
        tar.extractall(path = results_dir)
        tar.close()
        f = open(results_dir + "/results.json", "r")
        results = json.loads(f.read())
        f.close()
        errors = list()
        for contract in results:
            max_instruction_coverage = results[contract]["code_coverage"]["percentage"]
            max_branch_coverage = results[contract]["branch_coverage"]["percentage"]
            instruction_coverage.append(max_instruction_coverage)
            branch_coverage.append(max_branch_coverage)
            memory_consumption.append(results[contract]["memory_consumption"])
            execution_time.append(results[contract]["execution_time"])
            for generation in results[contract]["generations"]:
                if generation["code_coverage"] == max_instruction_coverage:
                    time_max_instruction_coverage.append(generation["time"])
                    break
            for generation in results[contract]["generations"]:
                if generation["branch_coverage"] == max_branch_coverage:
                    time_max_branch_coverage.append(generation["time"])
                    break
            transactions_per_second.append(results[contract]["transactions"]["per_second"])
            percentage_unique_transactions.append(results[contract]["generations"][-1]["unique_transactions"] / results[contract]["generations"][-1]["total_transactions"])
            if results[contract]["errors"] != {}:
                time = -1
                for n in results[contract]["errors"]:
                    for error in results[contract]["errors"][n]:
                        if time == -1:
                            time_bug.append(error["time"])
                            time = error["time"]
                        if "line" in error:
                            errors.append([error["type"], error["line"]])
                        else:
                            errors.append(error["type"])
                for generation in results[contract]["generations"]:
                    if generation["time"] > time:
                        total_transaction_bug.append(generation["total_transactions"])
                        unique_transactions_bug.append(generation["unique_transactions"])
                        break
        fw.write("{} - {}\n".format(contract_dir, errors))
        total_errors += len(errors)

    fw.write("Total errors: {}\n".format(total_errors))
    fw.write("\n")

    fw.write("----- Mean -----\n")
    fw.write("Instruction coverage: {}\n".format(statistics.mean(instruction_coverage)))
    fw.write("Branch coverage: {}\n".format(statistics.mean(branch_coverage)))
    fw.write("Time to final instruction coverage (s): {}\n".format(statistics.mean(time_max_instruction_coverage)))
    fw.write("Time to final branch coverage (s): {}\n".format(statistics.mean(time_max_branch_coverage)))
    fw.write("Time to bug (s): {}\n".format(statistics.mean(time_bug)))
    fw.write("Total transaction to bug: {}\n".format(statistics.mean(total_transaction_bug)))
    fw.write("Unique transaction to bug: {}\n".format(statistics.mean(unique_transactions_bug)))
    fw.write("Transactions executed per second: {}\n".format(statistics.mean(transactions_per_second)))
    fw.write("Percentage of unique transactions generated: {}\n".format(statistics.mean(percentage_unique_transactions) * 100))
    fw.write("Memory consumption (MB): {}\n".format(statistics.mean(memory_consumption)))
    fw.write("Execution time (s): {}\n".format(statistics.mean(execution_time)))

    fw.write("\n")
    fw.write("----- Standard Deviation -----\n")
    fw.write("Instruction coverage: {}\n".format(statistics.pstdev(instruction_coverage)))
    fw.write("Branch coverage: {}\n".format(statistics.pstdev(branch_coverage)))
    fw.write("Time to final instruction coverage (s): {}\n".format(statistics.pstdev(time_max_instruction_coverage)))
    fw.write("Time to final branch coverage (s): {}\n".format(statistics.pstdev(time_max_branch_coverage)))
    fw.write("Time to bug (s): {}\n".format(statistics.pstdev(time_bug)))
    fw.write("Total transaction to bug: {}\n".format(statistics.pstdev(total_transaction_bug)))
    fw.write("Unique transaction to bug: {}\n".format(statistics.pstdev(unique_transactions_bug)))
    fw.write("Transactions executed per second: {}\n".format(statistics.pstdev(transactions_per_second)))
    fw.write("Percentage of unique transactions generated: {}\n".format(statistics.pstdev(percentage_unique_transactions) * 100))
    fw.write("Memory consumption (MB): {}\n".format(statistics.pstdev(memory_consumption)))
    fw.write("Execution time (s): {}\n".format(statistics.pstdev(execution_time)))
    fw.close()