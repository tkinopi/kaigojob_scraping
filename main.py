from component import*

def main():

    flat_urls = get_urls()
    # print(flat_urls)
    # flat_urls = ['https://www.kaigoagent.com/job/46473', 'https://www.kaigoagent.com/job/365644','https://www.kaigoagent.com/job/365644',]
    # Flatten the list using a list comprehension
    # flat_urls = [url for sublist in nested_urls for url in sublist]
    # print(flat_urls)
    # flat_urls = get_sheet_a_data()
    print(flat_urls)
    jobs = []
    for url in flat_urls:
        result_dict = get_job_info(url)
        jobs.append(result_dict)
    print(jobs)
    write_to_spreadsheet(jobs)


if __name__ == "__main__":
    main()